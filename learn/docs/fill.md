<img src="https://www.notion.so/icons/water_pink.svg?mode=dark" width="80" alt="Wrench icon" />

# Fill
Fill a dictionary or dataclass with your data. If value is unknown, returns `None` or it's not included at all.

## 🍕 Descriptive dicts
Descriptive dictionaries are dictionaries with string-wrapped type annotations. Example:

```python
ai.give(bio_data).fill({
    "name": "str, Name of the person",
    "age": "int, Age of the person",
    "socials": {
        "linkedin": "str",
        "github": "str",
        "youtube": "str"
    }
})
```

## 💽 Dataclasses
Dataclasses are more structured and typed. Example:

```python
from dataclasses import dataclass

@dataclass
class MenuItem:
    name: str
    excerpt: str

@dataclass
class Cafe:
    name: str
    address: str
    phone: str
    website: str
    menu: list[MenuItem]

# Returns the `Cafe` dataclass.
cafe = ai.give(cafe_data).fill(Cafe)
```
