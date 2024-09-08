from aism import Aism, aifunc, messaged


@aifunc
def fan(mode: str) -> str:
    """Turn the fan on/off.

    Args:
        mode ("on" | "off"): The mode to set the fan to.
    """
    return "fan has been turned " + mode


ai = Aism()
fai = ai.function_ai([fan])

fai.guided_call(
    [messaged("user", "im... so... cold... the wind of the fan is so strong...")]
)
