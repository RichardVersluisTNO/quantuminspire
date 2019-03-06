from unittest import TestCase
from unittest.mock import Mock
from collections import OrderedDict
from coreapi.exceptions import ErrorMessage

from quantuminspire.job import QuantumInspireJob


class TestQuantumInspireJob(TestCase):

    def test_qi_job_invalid_api(self):
        api = Mock()
        job_identifier = 1
        self.assertRaises(ValueError, QuantumInspireJob, api, job_identifier)

    def test_qi_job_invalid_job_identifier(self):
        api = Mock()
        type(api).__name__ = 'QuantumInspireAPI'
        api.get_job.side_effect = ErrorMessage('TestMock')
        job_identifier = 1
        self.assertRaises(ValueError, QuantumInspireJob, api, job_identifier)
        api.get_job.called_once()

    def test_check_status(self):
        expected = 'RUNNING'
        api = Mock()
        api.get_job.return_value = {'status': expected}
        type(api).__name__ = 'QuantumInspireAPI'
        job_identifier = 1
        qi_job = QuantumInspireJob(api, job_identifier)
        actual = qi_job.check_status()
        self.assertEqual(expected, actual)

    def test_retrieve_result(self):
        expected = OrderedDict([('id', 502),
                                ('url', 'https,//api.quantum-inspire.com/results/502/'),
                                ('job', 'https,//api.quantum-inspire.com/jobs/10/'),
                                ('created_at', '1900-01-01T01:00:00:00000Z'),
                                ('number_of_qubits', 2),
                                ('seconds', 0.0),
                                ('raw_text', ''),
                                ('raw_data_url', 'https,//api.quantum-inspire.com/results/502/raw-data/f2b6/'),
                                ('histogram', {'3', 0.5068359375, '0', 0.4931640625}),
                                ('histogram_url', 'https,//api.quantum-inspire.com/results/502/histogram/f2b6/'),
                                ('measurement_mask', 0),
                                ('quantum_states_url',
                                 'https,//api.quantum-inspire.com/results/502/quantum-states/f2b6d/'),
                                ('measurement_register_url', 'https,//api.quantum-inspire.com/results/502/f2b6d/')])
        result_mock = Mock()
        api = Mock()
        api.get_job.return_value = {'results': result_mock}
        api.get.return_value = expected
        type(api).__name__ = 'QuantumInspireAPI'
        job_identifier = 1
        qi_job = QuantumInspireJob(api, job_identifier)
        actual = qi_job.retrieve_results()
        self.assertDictEqual(expected, actual)
        api.get_job.assert_called_with(job_identifier)
        api.get.assert_called_once_with(result_mock)

    def test_get_job_identifier(self):
        api = Mock()
        type(api).__name__ = 'QuantumInspireAPI'
        job_identifier = 1234
        qi_job = QuantumInspireJob(api, job_identifier)
        actual = qi_job.get_job_identifier()
        self.assertEqual(actual, job_identifier)

    def test_get_project_identifier(self):
        api = Mock()
        expected = 2
        asset = {'project_id': expected}
        type(api).__name__ = 'QuantumInspireAPI'
        api.get_job.return_value = {'input': asset}
        api.get.return_value = asset

        job_identifier = 1
        qi_job = QuantumInspireJob(api, job_identifier)
        actual = qi_job.get_project_identifier()
        self.assertEqual(expected, actual)
        api.get.assert_called_once_with(asset)
        api.get_job.assert_called_with(job_identifier)
