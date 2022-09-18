from mistune import HTMLRenderer, create_markdown, escape
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


class HighlightRenderer(HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ClassNotFound:
                pass
            else:
                formatter = HtmlFormatter()
                return highlight(code, lexer, formatter=formatter)
        return f"<pre><code>{escape(code)}</code></pre>"


markdown = create_markdown(renderer=HighlightRenderer())
