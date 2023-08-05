from schemazer.base import SchemazerSystemParameter
from commons.patterns import UUIDFormat
from validator import PatternValidator


class Systems:
    class Token(SchemazerSystemParameter):
        name = 'token'

        query_param = 'token'
        header_param = 'Auth-Token'
        cookie_param = 'auth_token'

        description = 'Access api key'
        type = str
        required = True
        example = '6b7f658a-0497-4885-9e48-d66002563923'
        validator = PatternValidator(UUIDFormat)
