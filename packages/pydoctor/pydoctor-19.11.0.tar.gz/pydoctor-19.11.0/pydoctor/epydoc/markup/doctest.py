#
# doctest.py: Syntax Highlighting for doctest blocks
# Edward Loper
#
# Created [06/28/03 02:52 AM]
#

"""
Syntax highlighting for doctest blocks.  This module defines the
function L{doctest_to_html()}, which can be used to perform syntax
highlighting on doctest blocks.  It also defines the more general
C{colorize_doctest()}, which could be used to do syntax highlighting
on doctest blocks with other output formats.
(C{doctest_to_html()} is defined using C{colorize_doctest()}.)
"""

from __future__ import print_function

__docformat__ = 'epytext en'

import re
from six.moves import builtins
from pydoctor.epydoc.util import plaintext_to_html

__all__ = ['doctest_to_html', 'HTMLDoctestColorizer']

def doctest_to_html(s):
    """
    Perform syntax highlighting on the given doctest string, and
    return the resulting HTML code.  This code consists of a C{<pre>}
    block with class=py-doctest.  Syntax highlighting is performed
    using the following css classes:

      - C{py-prompt} -- the Python PS1 prompt (>>>)
      - C{py-more} -- the Python PS2 prompt (...)
      - C{py-keyword} -- a Python keyword (for, if, etc.)
      - C{py-builtin} -- a Python builtin name (abs, dir, etc.)
      - C{py-string} -- a string literal
      - C{py-comment} -- a comment
      - C{py-except} -- an exception traceback (up to the next >>>)
      - C{py-output} -- the output from a doctest block.
      - C{py-defname} -- the name of a function or class defined by
        a C{def} or C{class} statement.
    """
    return HTMLDoctestColorizer().colorize_doctest(s)

class HTMLDoctestColorizer:
    """
    A class for performing syntax highlighting on doctest blocks
    and other bits of Python code.  Generates HTML output.
    """

    #: A string that is added to the beginning of the strings
    #: returned by L{colorize_codeblock} and L{colorize_doctest}.
    #: Typically, this string begins a preformatted area.
    PREFIX = '<pre class="py-doctest">\n'

    #: A string that is added to the end of the strings
    #: returned by L{colorize_codeblock} and L{colorize_doctest}.
    #: Typically, this string ends a preformatted area.
    SUFFIX = '</pre>\n'

    #: The string used to divide lines
    NEWLINE = '\n'

    #: A list of the names of all Python keywords.  ('as' is included
    #: even though it is technically not a keyword.)
    _KEYWORDS = ("and       del       for       is        raise"
                 "assert    elif      from      lambda    return"
                 "break     else      global    not       try"
                 "class     except    if        or        while"
                 "continue  exec      import    pass      yield"
                 "def       finally   in        print     as").split()

    #: A list of all Python builtins.
    _BUILTINS = [_BI for _BI in dir(builtins)
                 if not _BI.startswith('__')]

    #: A regexp group that matches keywords.
    _KEYWORD_GRP = '|'.join([r'\b%s\b' % _KW for _KW in _KEYWORDS])

    #: A regexp group that matches Python builtins.
    _BUILTIN_GRP = (r'(?<!\.)(?:%s)' % '|'.join([r'\b%s\b' % _BI
                                                 for _BI in _BUILTINS]))

    #: A regexp group that matches Python strings.
    _STRING_GRP = '|'.join(
        [r'("""("""|.*?((?!").)"""))', r'("("|.*?((?!").)"))',
         r"('''('''|.*?[^\\']'''))", r"('('|.*?[^\\']'))"])

    #: A regexp group that matches Python comments.
    _COMMENT_GRP = '(#.*?$)'

    #: A regexp group that matches Python ">>>" prompts.
    _PROMPT1_GRP = r'^[ \t]*>>>(?:[ \t]|$)'

    #: A regexp group that matches Python "..." prompts.
    _PROMPT2_GRP = r'^[ \t]*\.\.\.(?:[ \t]|$)'

    #: A regexp group that matches function and class definitions.
    _DEFINE_GRP = r'\b(?:def|class)[ \t]+\w+'

    #: A regexp that matches Python prompts
    PROMPT_RE = re.compile('(%s|%s)' % (_PROMPT1_GRP, _PROMPT2_GRP),
                           re.MULTILINE | re.DOTALL)

    #: A regexp that matches Python "..." prompts.
    PROMPT2_RE = re.compile('(%s)' % _PROMPT2_GRP,
                            re.MULTILINE | re.DOTALL)

    #: A regexp that matches doctest exception blocks.
    EXCEPT_RE = re.compile(r'^[ \t]*Traceback \(most recent call last\):.*',
                           re.DOTALL | re.MULTILINE)

    #: A regexp that matches doctest directives.
    DOCTEST_DIRECTIVE_RE = re.compile(r'#[ \t]*doctest:.*')

    #: A regexp that matches all of the regions of a doctest block
    #: that should be colored.
    DOCTEST_RE = re.compile(
        r'(.*?)((?P<STRING>%s)|(?P<COMMENT>%s)|(?P<DEFINE>%s)|'
              r'(?P<KEYWORD>%s)|(?P<BUILTIN>%s)|'
              r'(?P<PROMPT1>%s)|(?P<PROMPT2>%s)|(?P<EOS>\Z))' % (
        _STRING_GRP, _COMMENT_GRP, _DEFINE_GRP, _KEYWORD_GRP, _BUILTIN_GRP,
        _PROMPT1_GRP, _PROMPT2_GRP), re.MULTILINE | re.DOTALL)

    #: This regular expression is used to find doctest examples in a
    #: string.  This is copied from the standard Python doctest.py
    #: module (after the refactoring in Python 2.4+).
    DOCTEST_EXAMPLE_RE = re.compile(r'''
        # Source consists of a PS1 line followed by zero or more PS2 lines.
        (?P<source>
            (?:^(?P<indent> [ ]*) >>>    .*)    # PS1 line
            (?:\n           [ ]*  \.\.\. .*)*   # PS2 lines
          \n?)
        # Want consists of any non-blank lines that do not start with PS1.
        (?P<want> (?:(?![ ]*$)    # Not a blank line
                     (?![ ]*>>>)  # Not a line starting with PS1
                     .*$\n?       # But any other line
                  )*)
        ''', re.MULTILINE | re.VERBOSE)

    def colorize_inline(self, s):
        """
        Colorize a string containing Python code.  Do not add the
        L{PREFIX} and L{SUFFIX} strings to the returned value.  This
        method is intended for generating syntax-highlighted strings
        that are appropriate for inclusion as inline expressions.
        """
        return self.DOCTEST_RE.sub(self.subfunc, s)

    def colorize_codeblock(self, s):
        """
        Colorize a string containing only Python code.  This method
        differs from L{colorize_doctest} in that it will not search
        for doctest prompts when deciding how to colorize the string.
        """
        body = self.DOCTEST_RE.sub(self.subfunc, s)
        return self.PREFIX + body + self.SUFFIX

    def colorize_doctest(self, s, strip_directives=False):
        """
        Colorize a string containing one or more doctest examples.
        """
        output = []
        charno = 0
        for m in self.DOCTEST_EXAMPLE_RE.finditer(s):
            # Parse the doctest example:
            pysrc, want = m.group('source', 'want')
            # Pre-example text:
            output.append(self.NEWLINE.join(s[charno:m.start()].split('\n')))
            # Example source code:
            output.append(self.DOCTEST_RE.sub(self.subfunc, pysrc))
            # Example output:
            if want:
                if self.EXCEPT_RE.match(want):
                    output += self.NEWLINE.join([self.markup(line, 'except')
                                                 for line in want.split('\n')])
                else:
                    output += self.NEWLINE.join([self.markup(line, 'output')
                                                 for line in want.split('\n')])
            # Update charno
            charno = m.end()
        # Add any remaining post-example text.
        output.append(self.NEWLINE.join(s[charno:].split('\n')))

        return self.PREFIX + ''.join(output) + self.SUFFIX

    def subfunc(self, match):
        other, text = match.group(1, 2)
        #print('M %20r %20r' % (other, text)) # <- for debugging
        if other:
            other = self.NEWLINE.join([self.markup(line, 'other')
                                       for line in other.split('\n')])

        if match.group('PROMPT1'):
            return other + self.markup(text, 'prompt')
        elif match.group('PROMPT2'):
            return other + self.markup(text, 'more')
        elif match.group('KEYWORD'):
            return other + self.markup(text, 'keyword')
        elif match.group('BUILTIN'):
            return other + self.markup(text, 'builtin')
        elif match.group('COMMENT'):
            return other + self.markup(text, 'comment')
        elif match.group('STRING') and '\n' not in text:
            return other + self.markup(text, 'string')
        elif match.group('STRING'):
            # It's a multiline string; colorize the string & prompt
            # portion of each line.
            pieces = []
            for line in text.split('\n'):
                if self.PROMPT2_RE.match(line):
                    if len(line) > 4:
                        pieces.append(self.markup(line[:4], 'more') +
                                      self.markup(line[4:], 'string'))
                    else:
                        pieces.append(self.markup(line[:4], 'more'))
                elif line:
                    pieces.append(self.markup(line, 'string'))
                else:
                    pieces.append('')
            return other + self.NEWLINE.join(pieces)
        elif match.group('DEFINE'):
            m = re.match('(?P<def>\w+)(?P<space>\s+)(?P<name>\w+)', text)
            return other + (self.markup(m.group('def'), 'keyword') +
                        self.markup(m.group('space'), 'other') +
                        self.markup(m.group('name'), 'defname'))
        elif match.group('EOS') is not None:
            return other
        else:
            assert 0, 'Unexpected match!'

    def markup(self, s, tag):
        """
        Apply syntax highlighting to a single substring from a doctest
        block.  C{s} is the substring, and C{tag} is the tag that
        should be applied to the substring.  C{tag} will be one of the
        following strings:

          - C{prompt} -- the Python PS1 prompt (>>>)
          - C{more} -- the Python PS2 prompt (...)
          - C{keyword} -- a Python keyword (for, if, etc.)
          - C{builtin} -- a Python builtin name (abs, dir, etc.)
          - C{string} -- a string literal
          - C{comment} -- a comment
          - C{except} -- an exception traceback (up to the next >>>)
          - C{output} -- the output from a doctest block.
          - C{defname} -- the name of a function or class defined by
            a C{def} or C{class} statement.
          - C{other} -- anything else (does *not* include output.)
        """
        if tag == 'other':
            return plaintext_to_html(s)
        else:
            return ('<span class="py-%s">%s</span>' %
                    (tag, plaintext_to_html(s)))
