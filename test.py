from dataclasses import dataclass
from aism import Aism

ai = Aism()


@dataclass
class Verb:
    original_form: str
    positive: bool


@dataclass
class Content:
    verbs: list[Verb]


print(ai.give("Chocolate is amazing! In fact, it tastes awesome!").fill(Content))
