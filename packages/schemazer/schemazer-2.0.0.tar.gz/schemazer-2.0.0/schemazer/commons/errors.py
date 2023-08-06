"""
Module with errors group for fast access to error objects.
"""
from schemazer.base import SchemazerErrorGroup, SchemazerErrorBase


class RequestErrors(SchemazerErrorGroup):
    """ Simple request errors. """
    __group_name__ = 'RequestErrors'

    BadRequest = SchemazerErrorBase(
        group_name=__group_name__,
        name='BadRequest',
        description='Bad request',
    )
    NotFound = SchemazerErrorBase(
        group_name=__group_name__,
        name='NotFound',
        description='Object not found',
    )
    Undefined = SchemazerErrorBase(
        group_name=__group_name__,
        name='Undefined',
        description='Undefined error',
    )
