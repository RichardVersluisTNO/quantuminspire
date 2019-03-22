"""
This example is copied from https://github.com/ProjectQ-Framework/ProjectQ
and is covered under the Apache 2.0 license.
"""

import os
from getpass import getpass

from projectq import MainEngine
from projectq.backends import ResourceCounter
from projectq.ops import CNOT, H, Measure, All
from projectq.setups import restrictedgateset

from quantuminspire.credentials import load_token, get_token_authentication, get_basic_authentication
from quantuminspire.api import QuantumInspireAPI
from quantuminspire.projectq.backend_qx import QIBackend

QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')


def get_authentication():
    """ Gets the authentication for connecting to the Quantum Inspire API."""
    token = load_token()
    if token is not None:
        return get_token_authentication(token)
    else:
        if QI_EMAIL is None or QI_PASSWORD is None:
            print('Enter email:')
            email = input()
            print('Enter password')
            password = getpass()
        else:
            email, password = QI_EMAIL, QI_PASSWORD
        return get_basic_authentication(email, password)


if __name__ == '__main__':

    name = 'TestProjectQ'
    uri = r'https://api.quantum-inspire.com/'
    authentication = get_authentication()
    qi_api = QuantumInspireAPI(uri, authentication, project_name=name)

    compiler_engines = restrictedgateset.get_engine_list(one_qubit_gates="any", two_qubit_gates=(CNOT,))
    compiler_engines.extend([ResourceCounter()])

    qi_backend = QIBackend(quantum_inspire_api=qi_api)
    engine = MainEngine(backend=qi_backend, engine_list=compiler_engines)

    qubits = engine.allocate_qureg(2)
    q1 = qubits[0]
    q2 = qubits[1]

    H | q1
    CNOT | (q1, q2)
    All(Measure) | qubits

    engine.flush()

    print('\nMeasured: {0}'.format([int(q) for q in qubits]))
    print('Probabilities {0}'.format(qi_backend.get_probabilities(qubits)))
