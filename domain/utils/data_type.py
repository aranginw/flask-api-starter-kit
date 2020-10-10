"""Data Type to communication between components."""

import typing as t

from functools import reduce

from typeguard import check_type

T = t.TypeVar("T", bound="DataType")
U = t.TypeVar("U", bound="DataType")


class DataTypeInstantiationError(TypeError):
    """DataType instantiation attempted with incorrect attributes."""


class DataTypeExtraAttributesError(TypeError):
    """Attribute passed in weren's specified in the DataType."""


class DataType:
    """Fundamental class used for communication between components."""

    @classmethod
    def _get_annotations(cls) -> t.Dict[str, t.Any]:
        """Get annotations from any class and from any parents."""
        return reduce(
            lambda acc, kls: {**acc, **getattr(kls, "__annotations__", {})},
            reversed(cls.__mro__),
            {},
        )

    @classmethod
    def from_dict(cls: t.Type[T], dictionary: t.Dict[str, t.Any]) -> T:
        """Return a new DataType populated with data in dictionary."""
        annotations = cls._get_annotations()
        return cls(
            **dict(
                map(
                    lambda k: (k, dictionary[k]),
                    filter(lambda k: k in annotations, dictionary),
                )
            )
        )

    @classmethod
    def from_other(cls: t.Type[T], other: T) -> T:
        """Return a new DataType using another DataType instance."""
        return cls.from_dict(other.to_dict())

    @classmethod
    def from_other_with_updates(
        cls: t.Type[T], other: T, **updates: t.Any
    ) -> T:
        """Return a new DataType based on another DataType with overrides."""
        return cls.from_dict({**other.to_dict(), **updates})

    def to_dict(self) -> t.Dict[str, t.Any]:
        """Return a dictionary populated with data from DataType."""
        return {k: getattr(self, k) for k in self._get_annotations()}

    def __init__(self, *_: t.Any, **kwargs: t.Any) -> None:
        """Set attributes."""
        if not hasattr(self.__class__, "__annotations__"):
            raise DataTypeInstantiationError(
                f"{self.__class__.__name__}: you must specify attributes "
                "with type annotations in order to create a DataType"
            )
        self._annotations = self._get_annotations()
        extra_keys = tuple(filter(lambda k: k not in self._annotations, kwargs))
        if extra_keys:
            raise DataTypeExtraAttributesError(
                f"{self.__class__.__name__}: '{extra_keys}' not available to be set for this type"
            )

        inst_kwargs = {
            k: kwargs.get(k, getattr(self, k, None)) for k in self._annotations
        }

        for key, val in inst_kwargs.items():
            try:
                check_type(key, val, self._annotations[key])
            except TypeError:
                raise DataTypeInstantiationError(
                    f"{self.__class__.__name__}: '{key}' should be of type "
                    "{self._annotations[key]}, not {type(val)}"
                )
