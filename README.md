# aism (beta)
Let AI join your codebase. Integrate everything seamlessly.

```python
import aism

ra = aism.RustAism(api_key="gsk_xxx")  # Groq API key (leave blank for .env)

# Create a new instance
instance = ra.give("Mr. Beast just gave away a million dollars to the mayor.")
print(instance.is_sensitive())
print(instance.translate("chinese"))
print(instance.mentioned("what mr. beast did"))

# Fill the dictionary
print(
    instance.fill_dict({
        "subject": "The subject",
        "verb": "The verb",
        "topic": "What topic is this?"
    })
)
```
