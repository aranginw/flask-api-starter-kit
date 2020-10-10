"""Defines a domain User."""

from domain.utils.data_type import DataType


class User(DataType):
    """The User domain model."""

    first_name: str
    last_name: str
    age: int
