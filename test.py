import aism

description = (
    "A soufflé is a delicate, airy delight, crafted from the finest ingredients. "
    "It boasts a light, fluffy texture, rising gracefully with a golden, crisp top. "
    "Served warm, it offers a luxurious experience with each spoonful, "
    "whether it's a sweet, indulgent chocolate or a savory, refined cheese. "
    "Each bite is a testament to culinary artistry and sophistication."
)

ra = aism.RustAism(debug=True)

print(
    ra.give(description)
    .give(
        "Welcome to Acme, where elegance meets innovation. Our chic, minimalist decor complements the artisanal dishes crafted with precision. The menu is a curated symphony of flavors—signature truffle risotto, delicate lobster bisque, and soufflés that float like clouds. From hand-poured coffees to decadent pastries, each bite and sip elevates your dining experience. At Acme, indulgence is an art."
    )
    .fill_dict(
        {
            "title": "str, Best suiting title",
            "summarization": "str",
            "textures": "list[str]",
            "place": "str",
            "menu": "list[str]"
        }
    )
)
