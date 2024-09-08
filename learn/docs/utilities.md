<img src="https://www.notion.so/icons/wrench_blue.svg?mode=dark" width="80" alt="Wrench icon" />

# Utilities
Versatile APIs. The specifications described below are inside of an `Instance()` block, and is **NOT** within the main class `Aism()`.

Note that `self` in the arguments are omitted.


## 🈵 Translate

Translate the given data to the target language.

```python
translate(target: str) -> str
```

<details>
<summary><b>Example</b></summary>
    
```python
text = "Burgers taste like sandwiches."
ai.give(text).translate("Chinese")
```

</details>

## 🤬 Profanity check

Checks if the given data is sensitive.

> [!NOTE]
> 🚧 **This is still in beta**, internal prompting is subject to change.

```python
is_sensitive() -> bool
```

<details>
<summary><b>Example</b></summary>
    
```python
text = "F**k off, you little piece of..."
ai.give(text).is_sensitive()  # True
```

</details>

## 📍 Mentioned

Checks if the given resource is mentioned in the data.

> [!NOTE]
> 🚧 **This is still in beta**, internal prompting is subject to change.

```python
mentioned(target: str) -> bool
```

<details>
<summary><b>Example</b></summary>
    
```python
text = (
    "Sam Altman, the leader of OpenAI, "
    "just announced the release of an AI that eats strawberries."
)
ai.give(text).mentioned("who sam altman is")  # True
```

</details>

## 🎯 Matches

Checks if the data matches the description.

> [!NOTE]
> 🚧 **This is still in beta**, internal prompting is subject to change.

```python
matches(description: str) -> bool
```
