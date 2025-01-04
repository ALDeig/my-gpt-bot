import markdown2


def format_code(text: str) -> str:
    return (markdown2.markdown(text, extras=["fenced-code-blocks"]))
