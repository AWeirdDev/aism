import aism

ra = aism.RustAism()
instance = ra.give("Mr. Beast just gave away a million dollars to the mayor.")
# Fill the dictionary
print(
    instance.fill_dict({
        "subject": "The subject",
        "verb": "The verb",
        "topic": "What topic is this?"
    })
)