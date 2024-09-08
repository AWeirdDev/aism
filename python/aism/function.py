import inspect
import re
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Literal,
    ParamSpec,
    TypeVar,
    Union,
)

from .aism import RustAism
from .utils import messaged


FunctionReturnType = Union[str, int, dict, Literal[None]]


T = TypeVar("T", bound=FunctionReturnType)
P = ParamSpec("P")


class Function(Generic[P, T]):
    """Represents a callable function."""

    f: Callable[P, T]
    doc: Dict[str, Any]

    __slots__ = ("f", "doc")

    def __init__(self, f: Callable[P, T]):
        self.f = f
        self._mkdoc()
        self._checkdoc()

    def _mkdoc(self):
        """Make doc."""
        if not self.f.__doc__:
            raise ValueError(f"Expected docstring to be set for {self.f!r}, got None.")

        results = {"description": "", "args": {}}
        state = ""

        for line in self.f.__doc__.splitlines():
            if not line.strip():
                continue

            if line.strip().lower() == "args:":
                state = "args"

            elif line.strip().lower() == "returns:":
                break

            elif state == "args":
                res = re.findall(r"([^0-9\s]\w+)\s*(?:\((.+)\))?\s*:\s*(.+)", line)

                if not res:
                    raise ValueError(f"Unexpected docstring line: {line!r}")

                arg_name, type_, description = res[0]
                results["args"].update(
                    {arg_name: {"type": type_, "description": description}}
                )

            else:
                # normal doc
                results["description"] += f"{line.strip()}\n"

        self.doc = results

    def _checkdoc(self):
        """Check doc."""
        sig = inspect.signature(self.f)
        for name, param in sig.parameters.items():
            if name not in self.doc["args"]:
                raise ValueError(f"Missing docstring for {name!r} in {self.f!r}.")

            if param.kind == param.POSITIONAL_ONLY:
                raise TypeError("Positional-only parameters not yet supported.")

    def strdoc(self) -> str:
        """Stringify doc."""
        docs = []
        args = []
        for name, arg in self.doc["args"].items():
            args.append(name)
            docs.append(
                f"{name}: {arg['type']} - {arg['description'].replace('\n', ' ')}"
            )

        args_t = ", ".join(args)
        docs_t = "\n".join(docs)
        return f"{self.f.__name__}({args_t})\n{docs_t}"

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.f(*args, **kwargs)


def aifunc(c: Callable[P, T]) -> Function[P, T]:
    """Represents an AI-triggered function.

    .. note::

        Docstrings **MUST** be present.

    Example:
    .. code-block:: python

        @aifunc
        def add(a: int, b: int) -> int:
            \"\"\"Adds a and b.

            Args:
                a (int): The first number.
                b (int): The second number.

            Returns:
                int: The sum of a and b.
            \"\"\"
            return a + b

    Args:
        c (Callable[P, T]): The callable function.

    Returns:
        Function[P, T]: The wrapped function.
    """
    return Function(c)


class FunctionAI:
    """🎏 Function AI framework.

    Branched out from ``Aism`` as this does not require instances.

    Example:
    .. code-block:: python

        # Create a function-based AI instance
        fai = Aism().function_ai()  # or fai()
    """

    ra: RustAism
    functions: List[Function]

    def __init__(
        self,
        ra: RustAism,
        functions: List[Union[Function, Callable[..., FunctionReturnType]]],
    ):
        self.ra = ra
        self.functions = []

        for fn in functions:
            if not isinstance(fn, Function):
                fn = Function(fn)

            self.functions.append(fn)

    def guided_call(self, messages: List[dict]):
        instance = self.ra.give("Message history.").give(
            "Note: The last message is the newest."
        )

        result = instance._conv(
            [
                messaged(
                    "user",
                    "Given messages:\n"
                    + "\n".join(
                        [
                            msg["role"].replace("user", "User A")
                            + ": "
                            + msg["content"]
                            for msg in messages[-5:]
                        ]
                    )
                    + "Which of the function should be used to respond? What arguments should be passed? "
                    + "Are they all known in the conversation and can be used directly? Draft your response, and "
                    + "at the end of line, if your statement is to use a function, write the function call in the "
                    + "style of Python with parenthesis and commas separating the argument values; "
                    + "if your statement is to NOT use a function due to either the lack of known arguments or nothing "
                    + "should be used at all, write 'never'. Example for 'Yes, should call' and user said 'what is 1+3':\n"
                    + "The user wants to add numbers because they said 'what is 1+3', so "
                    + "I should use add(). The arguments a and b are known as the user wanted to perform 1 + 3, so "
                    + "a=1 and b=3. Therefore:\nadd(1, 3), because a and b are mentioned by the user."
                    + "\nExample for 'No, should not call due to lack of arguments' and user said 'i want to add numbers':\n"
                    + "I should not use add(). The user said 'I want to add numbers' but arguments are NOT explicitly "
                    + "mentioned. So, a is UNKNOWN, and b is UNKNOWN. Therefore:\n"
                    + "never, because the lack of arguments known\nExample for 'No, should not call due to non-related'\n"
                    + "The chat has never mentioned adding a number (originally the function 'add'), therefore:\n"
                    + "never, no functions should be called\n"
                    + "Available functions:\n"
                    + "\n".join([f.strdoc() for f in self.functions]),
                )
            ]
        )
        print(result)

        if result.splitlines()[-1].strip().split(",", 1)[0] == "never":
            return None
