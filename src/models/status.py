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
