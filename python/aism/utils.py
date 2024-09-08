import json
from dataclasses import Field, is_dataclass
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
    get_args,
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
    docs: Dict[str, Any] = {}

    for name, field in dc.__dataclass_fields__.items():
        origin = get_origin(field.type)
        args = get_args(field.type)

        if args and (origin is list or origin is List):
            docs[name] = [json.loads(t_name(args[0]))]

        elif is_dataclass(field.type):
            docs[name] = json.loads(dataclass_to_schema(field.type))

        elif field.type in NATIVE_TYPES:
            docs[name] = str(field.type)

        elif origin is Annotated:
            assert definitely(field.type, AnnotatedProtocol)
            docs[name] = t_name(args[0]) + f", {field.type.__metadata__[0]}"

        else:
            raise TypeError(f"Unrecognized type for {name!r}: {field.type}")

    return json.dumps(docs, indent=2)


def t_name(t: Any) -> str:
    if is_dataclass(t):
        return dataclass_to_schema(t)  # type: ignore
    else:
        return f"{repr(t)!r}"


def descriptive_dict_to_schema(dd: DescriptiveDict) -> str:
    return json.dumps(dd, indent=2)


DT = TypeVar("DT", bound=Dataclass)


def dict_to_schema(d: Dict[str, Any], dc: DT) -> DT:
    results = {}

    for k, v in d.items():
        origin = get_origin(dc.__dataclass_fields__[k].type)
        args = get_args(dc.__dataclass_fields__[k].type)

        if is_dataclass(dc.__dataclass_fields__[k].type):
            o = dc.__dataclass_fields__[k].type
            assert definitely(o, Dataclass)
            v = dict_to_schema(v, o)

        elif (origin is list or origin is List) and args and is_dataclass(args[0]):
            o = args[0]
            assert definitely(o, Dataclass)
            if isinstance(v, str):
                v = json.loads(v)
            v = [dict_to_schema(vi, o) for vi in v]

        results[k] = v

    return dc(**results)  # type: ignore
