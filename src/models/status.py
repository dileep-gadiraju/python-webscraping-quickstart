import enum


class Status(enum.Enum):
    SUCCESS = {
        'ok': True,
        'http': {'status': 200},
        'why': "request successful"
    }
    FAILURE = {
        'ok': False,
        'http': {'status': 500},
        'why': 'request failed'
    }
    ERR_SYSTEM = {
        'ok': False,
        'http': {'status': 500},
        'why': "Internal Server Error"
    }
    ERR_INVALID_DATA = {
        'ok': False,
        'http': {'status': 400},
        'why': "Invalid Data"
    }
    ERR_MISSING_PARAMETERS = {
        'ok': False,
        'http': {'status': 400},
        'why': "Data Missing"
    }
    CORRUPT_FILE = {
        'ok': False,
        'http': {'status': 500},
        'why': 'uploaded file is corrupt'
    }
    DATA_NOT_FOUND = {
        'ok': False,
        'http': {'status': 404},
        'why': 'data not found'
    }
    OPERATION_NOT_PERMITTED = {
        'ok': False,
        'http': {'status': 400},
        'why': 'operation not permitted'
    }
    ERR_GATEWAY = {
        'ok': False,
        'http': {'status': 400},
        'why': 'gateway error'
    }
    ERR_NOTFOUND_FILE = {
        'ok': False,
        'http': {'status': 400},
        'why': 'file not found'
    }
    ERR_SCHEMA_VALIDATION = {
        'ok': False,
        'http': {'status': 400},
        'why': 'please refer api contract to check your request structure'
    }
    ERR_TOO_MANY_REQUEST = {
        'ok': False,
        'http': {'status': 429},
        'why': 'too many requests'
    }


def get_status(exceptionType):
    e_dict = {
        'AgentError': Status.ERR_INVALID_DATA,
        'ParamMissing': Status.ERR_MISSING_PARAMETERS,
        'FormatError': Status.ERR_INVALID_DATA,
        'ValueMissing': Status.ERR_INVALID_DATA,
        'TooManyRequest': Status.ERR_TOO_MANY_REQUEST
    }
    if str(exceptionType) in e_dict.keys():
        status = e_dict[str(exceptionType)]
    else:
        status = Status.FAILURE
    return status
