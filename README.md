<div align="center">

![banner](weird_banner.png)

[GitHub](https://github.com/AWeirdDev/aism) ● [Workflows](https://github.com/AWeirdDev/aism/actions) ● [Issues](https://github.com/AWeirdDev/aism/issues)

`$ pip install aism`

</div>

So... what is Aism?

Aism provides a clean interface for summarizing, translating, conditional checks (like keypoint matching, mentioned checking), data auto-filling, <s>reordering</s>, <s>organizing</s>, <s>procedural data processing</s>, <s>function calling</s>, and more.<sup>1</sup>

**TL;DR: Aism is AI for the runtime.**

<sub><sup>1</sup> Striked-through features are currently in development and will be shipped within the next few months.</sub>

<h2>🧑‍🚀 3 Steps</h2>

<details>
<summary>Expand...</summary>

***

Aism is as simple as these 3 steps:

1. Get your Groq API key here: [console.groq.com](https://console.groq.com/keys)

2. Create your first AI runtime using the `Aism()` class.

```python
from aism import Aism

ai = Aism(
  api_key="YOUR_GROQ_API_KEY"  # optional. defaults to environment variable "GROQ_API_KEY"
)
```

3. Give any kind of data to the AI and play around with it.

```python
from dataclasses import dataclass

@dataclass
class News:
  title: str
  excerpt: str
  tags: list[str]

news = """\
A man in Springfield has reportedly trained his pet goldfish to understand basic calculus principles…
"""

# Give the data to the AI and fill it with the dataclass
print(ai.give(news).fill(News))
```

We get a nice result like this:

> 🐣 **Aism** <kbd>runtime</kbd>
> 
> ```python
> News(
>   title='A man in Springfield has reportedly trained his…', 
>   summarization='While skeptics abound, the fish has allegedly…', 
>   tags=['goldfish', 'calculus', 'Springfield']
> )
> ```

Awesome! Your data is **even more structured** and easier to understand through the typing system.

But wait, there's MORE to Aism?! Learn all about Aism in the `learn/` directory.

</details>


## 📚 Resources

- 🧠 [Learn](./learn/README.md) – The central of everything, perhaps.
- 📖 [Documentation](./learn/docs) – Refer to the API documentation and examples.
- 🥐 [Cookbooks](./learn/cookbooks) - Realistic use cases with notebooks.

***

(c) 2024 AWeirdDev
