from typing import cast

import markdown2
import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name


class HighlightRenderer(mistune.HTMLRenderer):
    """A custom renderer that highlights code blocks using Pygments."""

    def block_code(self, code: str, info: str | None = None):  # noqa: PLR6301
        if info:
            lexer = get_lexer_by_name(info, stripall=True)
            formatter = html.HtmlFormatter(wrapcode=True)
            return highlight(code, lexer, formatter)
        return "<pre><code>" + mistune.escape(code) + "</code></pre>"


def format_code_use_mistune(text: str) -> str:
    markdown = mistune.create_markdown(renderer=HighlightRenderer())
    return cast("str", markdown(text))


def format_code(text: str) -> str:
    return markdown2.markdown(text, extras=["fenced-code-blocks"])
