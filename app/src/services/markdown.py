import re


def escape_special_characters_in_place_text(text: str) -> str:
    result_text = ""
    pattern = re.compile(r"(```[^```]*```|`[^`]*`)", flags=re.DOTALL)
    status = "plane"
    for part in pattern.split(text):
        if status == "plane":
            result_text += _replace_symbols(part)
            status = "code"
        else:
            result_text += part
            status = "plane"
    return result_text


def _replace_symbols(text: str) -> str:
    symbols = [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "<",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]
    for symbol in symbols:
        text = text.replace(symbol, f"\\{symbol}")
    return text
