import json
from dataclasses import Field
from typing import (
    Annotated,
    Any,
    Dict,
    List,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_origin,
)

from typing_extensions import TypeGuard

DescriptiveDict = Dict[str, Union[str, "DescriptiveDict", List["DescriptiveDict"]]]
NATIVE_TYPES = {str, int, float, bool, list, dict}

T = TypeVar("T")


def definitely(__obj: Any, __t: Type[T]) -> TypeGuard[T]:
    return True


class Dataclass(Protocol):
    """Dataclass protocol."""

    __dataclass_fields__: Dict[str, Field]

    def __init__(self, *_, **__): ...


class AnnotatedProtocol(Protocol):
    """Annotated protocol."""

    __metadata__: Tuple[str, ...]
    __args__: Tuple[Type, ...]


def dataclass_to_schema(dc: Dataclass) -> str:
    docs: Dict[str, str] = {}

    for name, field in dc.__dataclass_fields__.items():
        origin = get_origin(field.type)
        if field.type in NATIVE_TYPES or origin in NATIVE_TYPES:
            docs.update({name: repr(field.type)})

        elif origin is Annotated:
            assert definitely(field.type, AnnotatedProtocol)
            docstring = field.type.__metadata__[0]
            docs.update({name: f"{repr(field.type.__args__[0])}, {docstring}"})

        else:
            raise TypeError(f"Unrecognized type for {name!r}: {field.type}")

    return json.dumps(docs, indent=2)


def descriptive_dict_to_schema(dd: DescriptiveDict) -> str:
    return json.dumps(dd, indent=2)
