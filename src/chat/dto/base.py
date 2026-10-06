from dataclasses import dataclass, fields
from typing import Self

from sqlalchemy import inspect

from core.models.base import Base


@dataclass(frozen=True)
class BaseDTO:
    def __post_init__(self) -> None:
        if type(self) is BaseDTO:
            raise TypeError("BaseDTO cannot be instantiated directly")

    @classmethod
    def from_orm_object(cls, obj: Base) -> Self:
        dto_fields = {field.name for field in fields(cls)}

        return cls(
            **{
                attr.key: getattr(obj, attr.key)
                for attr in inspect(obj).mapper.column_attrs
                if attr.key in dto_fields
            }
        )