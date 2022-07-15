from flask import jsonify


class RestAPIError(Exception):
    def __init__(self, status_code=500, payload=None):
        self.status_code = status_code
        self.payload = payload

    def to_response(self):
        return jsonify({'error': self.payload}), self.status_code


class BadRequestError(RestAPIError):
    def __init__(self, payload=None):
        super().__init__(400, payload)


class InternalServerError(RestAPIError):
    def __init__(self, payload=None):
        super().__init__(500, payload)


class AgentError(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def __str__(self):
        return self.message

class TooManyRequest(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def __str__(self):
        return self.message


class LoginFailure(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def __str__(self):
        return self.message


class ConnectionError(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def __str__(self):
        return self.message


class ParamMissing(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def __str__(self):
        return self.message


class FormatError(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def __str__(self):
        return self.message


class ValueMissing(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def __str__(self):
        return self.message


class ProxyFailure(Exception):
    def __init__(self, region):
        self.region = region

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value

    def __str__(self):
        return 'Proxy failure | region : {0}'.format(self.region)
