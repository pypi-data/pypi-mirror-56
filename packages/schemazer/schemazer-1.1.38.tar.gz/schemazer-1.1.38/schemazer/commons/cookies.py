from schemazer.base import SchemazerCookie
from commons.patterns import UUIDFormat
from validator import PatternValidator


class AuthCookies:
    class Apikey(SchemazerCookie):
        name = 'apikey'
        description = 'Access api key'
        type = str
        required = True
        example = '6b7f658a-0497-4885-9e48-d66002563923'
        validator = PatternValidator(UUIDFormat)
