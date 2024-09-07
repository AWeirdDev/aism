from dataclasses import dataclass
from aism import Aism


@dataclass
class Person:
    name: str


Aism().give("Hello, World").fill(Person)
