"""
Progress Bar.

pymdownx.progressbar
Simple plugin to add support for progress bars

```
/* No label */
[==30%]

/* Label */
[==30%  MyLabel]

/* works with attr_list inline style */
[==50/200  MyLabel]{: .additional-class }
```

New line is not required before the progress bar but suggested unless in a table.
Can take percentages and divisions.
Floats are okay.  Numbers must be positive.  This is an experimental extension.
Functionality is subject to change.

Minimum Recommended Styling
(but you could add gloss, candy striping, animation, or anything else):

```
.progress {
    display: block;
    width: 300px;
    margin: 10px 0;
    height: 24px;
    border: 1px solid #ccc;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    border-radius: 3px;
    background-color: #F8F8F8;
    position: relative;
    box-shadow: inset -1px 1px 3px rgba(0, 0, 0, .1);
}

.progress-label {
    position: absolute;
    text-align: center;
    font-weight: bold;
    width: 100%; margin: 0;
    line-height: 24px;
    color: #333;
    -webkit-font-smoothing: antialiased !important;
    white-space: nowrap;
    overflow: hidden;
}

.progress-bar {
    height: 24px;
    float: left;
    border-right: 1px solid #ccc;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    border-radius: 3px;
    background-color: #34c2e3;
    box-shadow: inset 0 1px 0px rgba(255, 255, 255, .5);
}

For Level Colors

.progress-100plus .progress-bar {
    background-color: #1ee038;
}

.progress-80plus .progress-bar {
    background-color: #86e01e;
}

.progress-60plus .progress-bar {
    background-color: #f2d31b;
}

.progress-40plus .progress-bar {
    background-color: #f2b01e;
}

.progress-20plus .progress-bar {
    background-color: #f27011;
}

.progress-0plus .progress-bar {
    background-color: #f63a0f;
}
```

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

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
from markdown.inlinepatterns import InlineProcessor, dequote
from markdown import util as md_util
from markdown.extensions.attr_list import AttrListTreeprocessor
from . import util

RE_PROGRESS = r'''(?x)
\[={1,}\s*                                                          # Opening
(?:
  (?P<percent>100(?:.0+)?|[1-9]?[0-9](?:\.\d+)?)% |                 # Percent
  (?:(?P<frac_num>\d+(?:\.\d+)?)\s*/\s*(?P<frac_den>\d+(?:\.\d+)?)) # Fraction
)
(?P<title>\s+(?P<quote>['"]).*?(?P=quote))?\s*                      # Title
\]                                                                  # Closing
(?P<attr_list>\{\:?([^\}]*)\})?                                     # Optional attr list
'''

CLASS_LEVEL = "progress-%dplus"


class ProgressBarTreeProcessor(AttrListTreeprocessor):
    """Used for AttrList compatibility."""

    def run(self, elem):
        """Inline check for attributes at start of tail."""

        if elem.tail:
            m = self.INLINE_RE.match(elem.tail)
            if m:
                self.assign_attrs(elem, m.group(1))
                elem.tail = elem.tail[m.end():]


class ProgressBarPattern(InlineProcessor):
    """Pattern handler for the progress bars."""

    def __init__(self, pattern, md):
        """Initialize."""

        InlineProcessor.__init__(self, pattern, md)

    def create_tag(self, width, label, add_classes, alist):
        """Create the tag."""

        # Create list of all classes and remove duplicates
        classes = list(
            set(
                ["progress"] +
                self.config.get('add_classes', '').split() +
                add_classes
            )
        )
        classes.sort()
        el = md_util.etree.Element("div")
        el.set('class', ' '.join(classes))
        bar = md_util.etree.SubElement(el, 'div')
        bar.set('class', "progress-bar")
        bar.set('style', 'width:%s%%' % width)
        p = md_util.etree.SubElement(bar, 'p')
        p.set('class', 'progress-label')
        p.text = label
        if alist is not None:
            el.tail = alist
            if 'attr_list' in self.md.treeprocessors:
                ProgressBarTreeProcessor(self.md).run(el)
        return el

    def handleMatch(self, m, data):
        """Handle the match."""

        label = ""
        level_class = self.config.get('level_class', False)
        increment = self.config.get('progress_increment', 20)
        add_classes = []
        alist = None
        if m.group(5):
            label = dequote(self.unescape(m.group('title').strip()))
        if m.group('attr_list'):
            alist = m.group('attr_list')
        if m.group('percent'):
            value = float(m.group('percent'))
        else:
            try:
                num = float(m.group('frac_num'))
            except Exception:  # pragma: no cover
                num = 0.0
            try:
                den = float(m.group('frac_den'))
            except Exception:  # pragma: no cover
                den = 0.0
            if den == 0.0:
                value = 0.0
            else:
                value = (num / den) * 100.0

        # We can never get a value < 0,
        # but we must check for > 100.
        if value > 100.0:
            value = 100.0

        # Round down to nearest increment step and include class if desired
        if level_class:
            add_classes.append(CLASS_LEVEL % int(value - (value % increment)))

        return self.create_tag('%.2f' % value, label, add_classes, alist), m.start(0), m.end(0)


class ProgressBarExtension(Extension):
    """Add progress bar extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'level_class': [
                True,
                "Include class that defines progress level - Default: True"
            ],
            'progress_increment': [
                20,
                "Progress increment step - Default: 20"
            ],
            'add_classes': [
                '',
                "Add additional classes to the progress tag for styling.  "
                "Classes are separated by spaces. - Default: None"
            ]
        }

        super(ProgressBarExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Add the progress bar pattern handler."""

        util.escape_chars(md, ['='])
        progress = ProgressBarPattern(RE_PROGRESS, md)
        progress.config = self.getConfigs()
        md.inlinePatterns.register(progress, "progress-bar", 179)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return ProgressBarExtension(*args, **kwargs)
