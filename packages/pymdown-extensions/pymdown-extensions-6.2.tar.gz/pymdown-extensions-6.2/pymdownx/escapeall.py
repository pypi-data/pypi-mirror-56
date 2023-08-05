"""
EscapeAll.

pymdownx.escapeall
Escape everything.

MIT license.

Copyright (c) 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import InlineProcessor, SubstituteTagInlineProcessor
from markdown.postprocessors import Postprocessor
from markdown import util as md_util
import re
from . import util

# We need to ignore these as they are used in Markdown processing
STX = '\u0002'
ETX = '\u0003'
ESCAPE_RE = r'\\(.)'
ESCAPE_NO_NL_RE = r'\\([^\n])'
HARDBREAK_RE = r'\\\n'
UNESCAPE_PATTERN = re.compile(r'%s(\d+)%s' % (md_util.STX, md_util.ETX))


class EscapeAllPattern(InlineProcessor):
    """Return an escaped character."""

    def __init__(self, pattern, nbsp):
        """Initialize."""

        self.nbsp = nbsp
        InlineProcessor.__init__(self, pattern)

    def handleMatch(self, m, data):
        """Convert the char to an escaped character."""

        char = m.group(1)
        if self.nbsp and char == ' ':
            escape = md_util.AMP_SUBSTITUTE + 'nbsp;'
        elif char in (STX, ETX):
            escape = char
        else:
            escape = '%s%s%s' % (md_util.STX, util.get_ord(char), md_util.ETX)
        return escape, m.start(0), m.end(0)


class EscapeAllPostprocessor(Postprocessor):
    """Post processor to strip out unwanted content."""

    def unescape(self, m):
        """Unescape the escaped chars."""

        return util.get_char(int(m.group(1)))

    def run(self, text):
        """Search document for escaped chars."""

        return UNESCAPE_PATTERN.sub(self.unescape, text)


class EscapeAllExtension(Extension):
    """Extension that allows you to escape everything."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'hardbreak': [
                False,
                "Turn escaped newlines to hardbreaks - Default: False"
            ],
            'nbsp': [
                False,
                "Turn escaped spaces to non-breaking spaces - Default: False"
            ]
        }
        super(EscapeAllExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Escape all."""

        config = self.getConfigs()
        hardbreak = config['hardbreak']
        md.inlinePatterns.register(
            EscapeAllPattern(ESCAPE_NO_NL_RE if hardbreak else ESCAPE_RE, config['nbsp']),
            "escape",
            180
        )

        md.postprocessors.register(EscapeAllPostprocessor(md), "unescape", 10)
        if config['hardbreak']:
            md.inlinePatterns.register(SubstituteTagInlineProcessor(HARDBREAK_RE, 'br'), "hardbreak", 5.1)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return EscapeAllExtension(*args, **kwargs)
