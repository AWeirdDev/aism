from dataclasses import is_dataclass
from typing import (
    Any,
    Dict,
    List,
    LiteralString,
    Optional,
    TypeVar,
    Union,
    overload,
)

from .aism import RustAism, RustInstance
from .utils import (
    Dataclass,
    DescriptiveDict,
    dataclass_to_schema,
    descriptive_dict_to_schema,
    dict_to_schema,
)


class Aism:
    """🗻 The Aism AI framework.

    Args:F
        api_key (str, optional): Your Groq API key. Defaults to ``None`` if using the environment variable
            ``GROQ_API_KEY``.
        debug (bool, optional): Whether to print debug messages. Defaults to ``False``.
    """

    ra: RustAism

    def __init__(self, *, api_key: Optional[str] = None, debug: bool = False):
        self.ra = RustAism(api_key=api_key, debug=debug)

    def give(self, data: str) -> "Instance":
        """Creates a new instance.

        Args:
            data (str): The data to provide.
        """
        return Instance(self.ra.give(data))

    def feed(self, rows: Union[List[str], List[LiteralString]]) -> "Instance":
        """Creates a new instance from a row of data.

        Args:
            rows (List[str]): The rows of data to provide.
        """
        return Instance(self.ra.feed(rows))  # type: ignore

    def solve_world_hunger(
        self, rows: Union[List[str], List[LiteralString]]
    ) -> "Instance":
        """You're a good person.

        Args:
            rows (List[str]): The rows of data to provide.
        """
        return Instance(self.ra.feed(rows))  # type: ignore

    def __repr__(self) -> str:
        return "Aism::<RustAism>()"


T_DescriptiveDC = TypeVar("T_DescriptiveDC", bound=Dataclass)


class Instance:
    """Represents an instance.

    .. note::

        This is an internal class and should not be constructed directly outside of the ecosystem.
    """

    def __init__(self, ri: RustInstance):
        self.ri = ri

    def give(self, data: str) -> "Instance":
        """Adds data to the current instance.

        Args:
            data (str): The data to provide.
        """
        return Instance(self.ri.give(data))

    def feed(self, rows: Union[List[str], List[LiteralString]]) -> "Instance":
        """Adds rows of data to the current instance.

        Args:
            rows (List[str]): The rows of data to provide.
        """
        return Instance(self.ri.feed(rows))  # type: ignore

    def instruct(self, instruction: str) -> str:
        """Instruct the LLM to complete the given instruction.

        Args:
            instruction (str): The instruction to fulfill.
        """
        return self.ri.instruct(instruction)

    def translate(self, language: str) -> str:
        """Translate the given text to the given language.

        Example:
        .. code-block:: python

            ai.give("Who made the souffle?").translate("french")
            # "Qui a fait la soufflé ?"

        Args:
            language (str): The language to translate to.
        """
        return self.ri.translate(language)

    def is_sensitive(self) -> bool:
        """Check if the instance is sensitive.

        Performs a profanity check.

        Example:
        .. code-block:: python

            ai.give("F**K.").is_sensitive()  # True
        """
        return self.ri.is_sensitive()

    def mentioned(self, keyword: str) -> bool:
        r"""Check if the instance mentions the given keyword.

        Example:
        .. code-block:: python

            ai \
                .give("Chocolate tastes amazing!")
                .mentioned("how chocolate tastes")
            # True

        Args:
            keyword (str): The keyword to check for.
        """
        return self.ri.mentioned(keyword)

    def matches(self, keyword: str) -> bool:
        """Check if the instance matches the given keyword.

        Example:
        .. code-block:: python

            ai.give("The quick brown fox jumps over the lazy dog.").matches("has a noun")

        Args:
            keyword (str): The keyword to check for.
        """
        return self.ri.matches(keyword)

    def summarize(self) -> str:
        """Summarize the instance.

        Example:
        .. code-block:: python

            text = "The soufflé. One spoonful and it simply melts, like a cloud cradling your taste buds in a whisper of sweetness."
            ai.give(text).summarize()
            # "The soufflé melts in the mouth, with a whisper of sweetness."

        """
        return self.ri.summarize()

    def summarise(self) -> str:
        """Summarise the instance.

        Alias for :func:`summarize`. If you're British, we've got you covered.
        """
        return self.summarize()

    @overload
    def fill(self, o: T_DescriptiveDC) -> T_DescriptiveDC:
        """Fill the instance data with the given dataclass.

        Example:
        .. code-block:: python

            from dataclasses import dataclass

            @dataclass
            class News:
                person: str
                tags: list[str]
                objects: list[str]

            ai.give(
                "Sam Altman just announced a special edition of strawberry ice cream because of the release of ChatGPT.",
                News
            )

        Args:
            o (Dataclass): The dataclass to fill with.
        """

    @overload
    def fill(self, o: DescriptiveDict) -> Dict[str, Any]:
        """Fill the instance data with the given descriptive dictionary.

        Example:
        .. code-block:: python

            ai.give(
                "Sam Altman just announced a special edition of strawberry ice cream because of the release of ChatGPT.",
                {
                    "person": "str, The person",
                    "tags": "list[str]",
                    "objects": "list[str]"
                }
            )

        Args:
            o (DescriptiveDict): The dictionary to fill with.
        """

    def fill(
        self, o: Union[Dataclass, DescriptiveDict]
    ) -> Union[Dict[str, Any], Dataclass]:
        if is_dataclass(o):
            desc = dataclass_to_schema(o)
            res = self.ri.fill_dict(desc + "\nProvide the best value for each key.")
            if len(res.keys()) == 1 and list(res)[0] == o.__name__:
                res = res[o.__name__]

            return dict_to_schema(res, o)

        elif isinstance(o, dict):
            desc = descriptive_dict_to_schema(o)
            res = self.ri.fill_dict(desc)

        else:
            raise TypeError(f"Unrecognized type for instance.fill: {type(o)}")

        return res
