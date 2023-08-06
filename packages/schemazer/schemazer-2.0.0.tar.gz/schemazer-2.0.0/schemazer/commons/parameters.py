from schemazer.base import SchemazerParameter
from schemazer.commons.patterns import (
    IntFormat, BaseFormat, FloatFormat, BooleanFormat, IntervalFormat
)
from schemazer.validator import PatternValidator
from schemazer.commons.interval import check_interval


class BaseParameters:
    class Integer(SchemazerParameter):
        name = 'number'
        description = 'Number'
        type = int
        converter = int
        required = False
        example = '125'
        validator = PatternValidator(IntFormat)

    class String(SchemazerParameter):
        name = 'string'
        description = 'string'
        type = str
        converter = str
        required = False
        example = 'string'
        validator = PatternValidator(BaseFormat)

    class Float(SchemazerParameter):
        name = 'float'
        description = 'float'
        type = float
        converter = float
        required = False
        example = 123.123
        validator = PatternValidator(FloatFormat)

    class Boolean(SchemazerParameter):
        @staticmethod
        def converter(value):
            return str(value).lower() in ['true', '1']

        name = 'bool'
        description = 'bool'
        type = bool
        required = False
        example = True
        validator = PatternValidator(BooleanFormat)

    class Interval(SchemazerParameter):
        name = 'interval'
        description = 'interval'
        type = str
        required = False
        example = '20,35'
        validator = PatternValidator(IntervalFormat)
        interval = check_interval
