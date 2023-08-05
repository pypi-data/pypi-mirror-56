from schemazer.base import SchemazerHeader
from commons.patterns import UUIDFormat
from validator import PatternValidator


class AuthHeaders:
    class Apikey(SchemazerHeader):
        name = 'Apikey'
        description = 'Access api key'
        type = str
        required = True
        example = '6b7f658a-0497-4885-9e48-d66002563923'
        validator = PatternValidator(UUIDFormat)
