# 🧪 aism (beta)
Let AI join your codebase. Integrate with everything seamlessly.

## Tutorial
So, what really *is* Aism? You'll see it for yourself. First things first, we'll create a new client using `RustAism` for the simplest features.

```python
import aism
ra = aism.RustAism(api_key="gsk_xxx")  # Groq API key
```

AI needs **data**. Therefore, you'll have to feed it through `give()` (as the name suggests, *give* it to the LLM).

```python
instance = ra.give("Chocolate tastes delicious, and sweet!")
```

This creates a new `RustInstance`, and your data is ready to be served (...to the LLM)!

Take a simple task for example, we can translate it:

```python
instance.translate("german")
```

You can also check if it is sensitive (like swear words):

```python
instance.is_sensitive()
```

Those are just the basic ones. What's more, you can tell it to fill a dict!

```python
instance.fill_dict({
  "title": "summarized title",
  "tastes": "how it tastes",
  "speaker": "who the speaker is"  # if unknown, gives None
})
```

You get a nice formatted dict!

<details>
<summary>Example</summary>

```python
{
  "title": "Delicious Chocolate",
  "tastes": "delicious and sweet",
  "speaker": None
}
```
  
</details>

***

To sum it up, Aism is **AI for the runtime**. How? Watch.

```python
def add_comment(content: str):
  if ra.give(content).is_sensitive():
    raise ValueError("content must not be sensitive!")
  fake_db.add_comment(content)
```

