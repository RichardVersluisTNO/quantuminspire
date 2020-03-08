""" Module introducing some custom Exceptions """


class QisKitBackendError(Exception):
    """ Exception for SDK errors related to the qiskit backend."""


class ProjectQBackendError(Exception):
    """ Exception for SDK errors related to the projectq backend."""


class AuthenticationError(Exception):
    """ Exception for SDK errors related to authentication."""


class ApiError(Exception):
    """ Exception for SDK errors related to the API functionality."""
