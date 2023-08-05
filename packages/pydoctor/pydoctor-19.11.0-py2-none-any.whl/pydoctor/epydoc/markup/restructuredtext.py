#
# rst.py: ReStructuredText docstring parsing
# Edward Loper
#
# Created [06/28/03 02:52 AM]
#

"""
Epydoc parser for ReStructuredText strings.  ReStructuredText is the
standard markup language used by the Docutils project.
L{parse_docstring()} provides the primary interface to this module; it
returns a L{ParsedRstDocstring}, which supports all of the methods
defined by L{ParsedDocstring}.

L{ParsedRstDocstring} is basically just a L{ParsedDocstring} wrapper
for the C{docutils.nodes.document} class.

Creating C{ParsedRstDocstring}s
===============================

C{ParsedRstDocstring}s are created by the C{parse_document} function,
using the C{docutils.core.publish_string()} method, with the following
helpers:

  - An L{_EpydocReader} is used to capture all error messages as it
    parses the docstring.
  - A L{_DocumentPseudoWriter} is used to extract the document itself,
    without actually writing any output.  The document is saved for
    further processing.  The settings for the writer are copied from
    C{docutils.writers.html4css1.Writer}, since those settings will
    be used when we actually write the docstring to html.

Using C{ParsedRstDocstring}s
============================

C{ParsedRstDocstring}s support all of the methods defined by
C{ParsedDocstring}; but only the following four methods have
non-default behavior:

  - L{to_html()<ParsedRstDocstring.to_html>} uses an
    L{_EpydocHTMLTranslator} to translate the C{ParsedRstDocstring}'s
    document into an HTML segment.
  - L{split_fields()<ParsedRstDocstring.split_fields>} uses a
    L{_SplitFieldsTranslator} to divide the C{ParsedRstDocstring}'s
    document into its main body and its fields.  Special handling
    is done to account for consolidated fields.

@var CONSOLIDATED_FIELDS: A dictionary encoding the set of
'consolidated fields' that can be used.  Each consolidated field is
marked by a single tag, and contains a single bulleted list, where
each list item starts with an identifier, marked as interpreted text
(C{`...`}).  This module automatically splits these consolidated
fields into individual fields.  The keys of C{CONSOLIDATED_FIELDS} are
the names of possible consolidated fields; and the values are the
names of the field tags that should be used for individual entries in
the list.
"""
__docformat__ = 'epytext en'

# Imports
import re

from docutils.core import publish_string
from docutils.writers import Writer
from docutils.writers.html4css1 import HTMLTranslator, Writer as HTMLWriter
from docutils.readers.standalone import Reader as StandaloneReader
from docutils.utils import new_document
from docutils.nodes import NodeVisitor, SkipNode
from docutils.frontend import OptionParser
from docutils.parsers.rst import directives, roles
import docutils.nodes
import docutils.transforms.frontmatter
import docutils.transforms
import docutils.utils

from pydoctor.epydoc.markup import Field, ParseError, ParsedDocstring
from pydoctor.epydoc.markup.plaintext import ParsedPlaintextDocstring
from pydoctor.epydoc.util import plaintext_to_html
from pydoctor.epydoc.markup.doctest import doctest_to_html, HTMLDoctestColorizer

#: A dictionary whose keys are the "consolidated fields" that are
#: recognized by epydoc; and whose values are the corresponding epydoc
#: field names that should be used for the individual fields.
CONSOLIDATED_FIELDS = {
    'parameters': 'param',
    'arguments': 'arg',
    'exceptions': 'except',
    'variables': 'var',
    'ivariables': 'ivar',
    'cvariables': 'cvar',
    'groups': 'group',
    'types': 'type',
    'keywords': 'keyword',
    }

#: A list of consolidated fields whose bodies may be specified using a
#: definition list, rather than a bulleted list.  For these fields, the
#: 'classifier' for each term in the definition list is translated into
#: a @type field.
CONSOLIDATED_DEFLIST_FIELDS = ['param', 'arg', 'var', 'ivar', 'cvar', 'keyword']

def parse_docstring(docstring, errors):
    """
    Parse the given docstring, which is formatted using
    ReStructuredText; and return a L{ParsedDocstring} representation
    of its contents.
    @param docstring: The docstring to parse
    @type docstring: C{string}
    @param errors: A list where any errors generated during parsing
        will be stored.
    @type errors: C{list} of L{ParseError}
    @rtype: L{ParsedDocstring}
    """
    writer = _DocumentPseudoWriter()
    reader = _EpydocReader(errors) # Outputs errors to the list.
    publish_string(docstring, writer=writer, reader=reader,
                   settings_overrides={'report_level':10000,
                                       'halt_level':10000,
                                       'warning_stream':None})
    return ParsedRstDocstring(writer.document)

class OptimizedReporter(docutils.utils.Reporter):
    """A reporter that ignores all debug messages.  This is used to
    shave a couple seconds off of epydoc's run time, since docutils
    isn't very fast about processing its own debug messages."""
    def debug(self, *args, **kwargs): pass

class ParsedRstDocstring(ParsedDocstring):
    """
    An encoded version of a ReStructuredText docstring.  The contents
    of the docstring are encoded in the L{_document} instance
    variable.

    @ivar _document: A ReStructuredText document, encoding the
        docstring.
    @type _document: C{docutils.nodes.document}
    """
    def __init__(self, document):
        """
        @type document: C{docutils.nodes.document}
        """
        self._document = document

        # The default document reporter and transformer are not
        # pickle-able; so replace them with stubs that are.
        document.reporter = OptimizedReporter(
            document.reporter.source, 'SEVERE', 'SEVERE', '')
        document.transformer = docutils.transforms.Transformer(document)

    def split_fields(self, errors=None):
        # Inherit docs
        if errors is None: errors = []
        visitor = _SplitFieldsTranslator(self._document, errors)
        self._document.walk(visitor)
        if len(self._document.children) > 0:
            return self, visitor.fields
        else:
            return None, visitor.fields

    def to_html(self, docstring_linker, directory=None,
                docindex=None, context=None):
        # Inherit docs
        visitor = _EpydocHTMLTranslator(self._document, docstring_linker,
                                        directory, docindex, context)
        self._document.walkabout(visitor)
        return ''.join(visitor.body)

    def __repr__(self): return '<ParsedRstDocstring: ...>'

class _EpydocReader(StandaloneReader):
    """
    A reader that captures all errors that are generated by parsing,
    and appends them to a list.
    """

    def __init__(self, errors):
        self._errors = errors
        StandaloneReader.__init__(self)

    def get_transforms(self):
        # Remove the DocInfo transform, to ensure that :author: fields
        # are correctly handled.
        return [t for t in StandaloneReader.get_transforms(self)
                if t != docutils.transforms.frontmatter.DocInfo]

    def new_document(self):
        document = new_document(self.source.source_path, self.settings)
        # Capture all warning messages.
        document.reporter.attach_observer(self.report)
        # These are used so we know how to encode warning messages:
        self._encoding = document.reporter.encoding
        self._error_handler = document.reporter.error_handler
        # Return the new document.
        return document

    def report(self, error):
        try: is_fatal = int(error['level']) > 2
        except: is_fatal = True
        try: linenum = int(error['line'])
        except: linenum = None

        msg = ''.join([c.astext().encode(self._encoding, self._error_handler)
                       for c in error])

        self._errors.append(ParseError(msg, linenum, is_fatal))

class _DocumentPseudoWriter(Writer):
    """
    A pseudo-writer for the docutils framework, that can be used to
    access the document itself.  The output of C{_DocumentPseudoWriter}
    is just an empty string; but after it has been used, the most
    recently processed document is available as the instance variable
    C{document}

    @type document: C{docutils.nodes.document}
    @ivar document: The most recently processed document.
    """
    def __init__(self):
        self.document = None
        Writer.__init__(self)

    def translate(self):
        self.output = ''

class _SplitFieldsTranslator(NodeVisitor):
    """
    A docutils translator that removes all fields from a document, and
    collects them into the instance variable C{fields}

    @ivar fields: The fields of the most recently walked document.
    @type fields: C{list} of L{Field<markup.Field>}
    """

    ALLOW_UNMARKED_ARG_IN_CONSOLIDATED_FIELD = True
    """If true, then consolidated fields are not required to mark
    arguments with C{`backticks`}.  (This is currently only
    implemented for consolidated fields expressed as definition lists;
    consolidated fields expressed as unordered lists still require
    backticks for now."""

    def __init__(self, document, errors):
        NodeVisitor.__init__(self, document)
        self._errors = errors
        self.fields = []
        self._newfields = set()

    def visit_document(self, node):
        self.fields = []

    def visit_field(self, node):
        # Remove the field from the tree.
        node.parent.remove(node)

        # Extract the field name & optional argument
        tag = node[0].astext().split(None, 1)
        tagname = tag[0]
        if len(tag)>1: arg = tag[1]
        else: arg = None

        # Handle special fields:
        fbody = node[1]
        if arg is None:
            for (list_tag, entry_tag) in CONSOLIDATED_FIELDS.items():
                if tagname.lower() == list_tag:
                    try:
                        self.handle_consolidated_field(fbody, entry_tag)
                        return
                    except ValueError as e:
                        estr = 'Unable to split consolidated field '
                        estr += '"%s" - %s' % (tagname, e)
                        self._errors.append(ParseError(estr, node.line,
                                                       is_fatal=False))

                        # Use a @newfield to let it be displayed as-is.
                        if tagname.lower() not in self._newfields:
                            newfield = Field('newfield', tagname.lower(),
                                             ParsedPlaintextDocstring(tagname))
                            self.fields.append(newfield)
                            self._newfields.add(tagname.lower())

        self._add_field(tagname, arg, fbody)

    def _add_field(self, tagname, arg, fbody):
        field_doc = self.document.copy()
        for child in fbody: field_doc.append(child)
        field_pdoc = ParsedRstDocstring(field_doc)
        self.fields.append(Field(tagname, arg, field_pdoc))

    def visit_field_list(self, node):
        # Remove the field list from the tree.  The visitor will still walk
        # over the node's children.
        node.parent.remove(node)

    def handle_consolidated_field(self, body, tagname):
        """
        Attempt to handle a consolidated section.
        """
        if len(body) != 1:
            raise ValueError('does not contain a single list.')
        elif body[0].tagname == 'bullet_list':
            self.handle_consolidated_bullet_list(body[0], tagname)
        elif (body[0].tagname == 'definition_list' and
              tagname in CONSOLIDATED_DEFLIST_FIELDS):
            self.handle_consolidated_definition_list(body[0], tagname)
        elif tagname in CONSOLIDATED_DEFLIST_FIELDS:
            raise ValueError('does not contain a bulleted list or '
                             'definition list.')
        else:
            raise ValueError('does not contain a bulleted list.')

    def handle_consolidated_bullet_list(self, items, tagname):
        # Check the contents of the list.  In particular, each list
        # item should have the form:
        #   - `arg`: description...
        n = 0
        _BAD_ITEM = ("list item %d is not well formed.  Each item must "
                     "consist of a single marked identifier (e.g., `x`), "
                     "optionally followed by a colon or dash and a "
                     "description.")
        for item in items:
            n += 1
            if item.tagname != 'list_item' or len(item) == 0:
                raise ValueError('bad bulleted list (bad child %d).' % n)
            if item[0].tagname != 'paragraph':
                if item[0].tagname == 'definition_list':
                    raise ValueError(('list item %d contains a definition '+
                                      'list (it\'s probably indented '+
                                      'wrong).') % n)
                else:
                    raise ValueError(_BAD_ITEM % n)
            if len(item[0]) == 0:
                raise ValueError(_BAD_ITEM % n)
            if item[0][0].tagname != 'title_reference':
                raise ValueError(_BAD_ITEM % n)

        # Everything looks good; convert to multiple fields.
        for item in items:
            # Extract the arg
            arg = item[0][0].astext()

            # Extract the field body, and remove the arg
            fbody = item[:]
            fbody[0] = fbody[0].copy()
            fbody[0][:] = item[0][1:]

            # Remove the separating ":", if present
            if (len(fbody[0]) > 0 and
                isinstance(fbody[0][0], docutils.nodes.Text)):
                text = fbody[0][0].astext()
                if text[:1] in ':-':
                    fbody[0][0] = docutils.nodes.Text(
                        text[1:].lstrip(), fbody[0][0].rawsource
                        )
                elif text[:2] in (' -', ' :'):
                    fbody[0][0] = docutils.nodes.Text(
                        text[2:].lstrip(), fbody[0][0].rawsource
                        )

            # Wrap the field body, and add a new field
            self._add_field(tagname, arg, fbody)

    def handle_consolidated_definition_list(self, items, tagname):
        # Check the list contents.
        n = 0
        _BAD_ITEM = ("item %d is not well formed.  Each item's term must "
                     "consist of a single marked identifier (e.g., `x`), "
                     "optionally followed by a space, colon, space, and "
                     "a type description.")
        for item in items:
            n += 1
            if (item.tagname != 'definition_list_item' or len(item) < 2 or
                item[0].tagname != 'term' or
                item[-1].tagname != 'definition'):
                raise ValueError('bad definition list (bad child %d).' % n)
            if len(item) > 3:
                raise ValueError(_BAD_ITEM % n)
            if not ((item[0][0].tagname == 'title_reference') or
                    (self.ALLOW_UNMARKED_ARG_IN_CONSOLIDATED_FIELD and
                     isinstance(item[0][0], docutils.nodes.Text))):
                raise ValueError(_BAD_ITEM % n)
            for child in item[0][1:]:
                if child.astext() != '':
                    raise ValueError(_BAD_ITEM % n)

        # Extract it.
        for item in items:
            # The basic field.
            arg = item[0][0].astext()
            fbody = item[-1]
            self._add_field(tagname, arg, fbody)
            # If there's a classifier, treat it as a type.
            if len(item) == 3:
                type_descr = item[1]
                self._add_field('type', arg, type_descr)

    def unknown_visit(self, node):
        'Ignore all unknown nodes'

_TARGET_RE = re.compile(r'^(.*?)\s*<(?:URI:|URL:)?([^<>]+)>$')

class _EpydocHTMLTranslator(HTMLTranslator):
    settings = None
    def __init__(self, document, docstring_linker, directory,
                 docindex, context):
        self._linker = docstring_linker
        self._directory = directory
        self._docindex = docindex
        self._context = context

        # Set the document's settings.
        if self.settings is None:
            settings = OptionParser([HTMLWriter()]).get_default_values()
            self.__class__.settings = settings
        document.settings = self.settings

        # Call the parent constructor.
        HTMLTranslator.__init__(self, document)

    # Handle interpreted text (crossreferences)
    def visit_title_reference(self, node):
        m = _TARGET_RE.match(node.astext())
        if m: text, target = m.groups()
        else: target = text = node.astext()
        text = plaintext_to_html(text)
        xref = self._linker.translate_identifier_xref(target, text)
        self.body.append(xref)
        raise SkipNode()

    def should_be_compact_paragraph(self, node):
        if self.document.children == [node]:
            return True
        else:
            return HTMLTranslator.should_be_compact_paragraph(self, node)

    def visit_document(self, node): pass
    def depart_document(self, node): pass

    def starttag(self, node, tagname, suffix='\n', **attributes):
        """
        This modified version of starttag makes a few changes to HTML
        tags, to prevent them from conflicting with epydoc.  In particular:
          - existing class attributes are prefixed with C{'rst-'}
          - existing names are prefixed with C{'rst-'}
          - hrefs starting with C{'#'} are prefixed with C{'rst-'}
          - hrefs not starting with C{'#'} are given target='_top'
          - all headings (C{<hM{n}>}) are given the css class C{'heading'}
        """
        # Get the list of all attribute dictionaries we need to munge.
        attr_dicts = [attributes]
        if isinstance(node, docutils.nodes.Node):
            attr_dicts.append(node.attributes)
        if isinstance(node, dict):
            attr_dicts.append(node)
        # Munge each attribute dictionary.  Unfortunately, we need to
        # iterate through attributes one at a time because some
        # versions of docutils don't case-normalize attributes.
        for attr_dict in attr_dicts:
            for (key, val) in attr_dict.items():
                # Prefix all CSS classes with "rst-"; and prefix all
                # names with "rst-" to avoid conflicts.
                if key.lower() in ('class', 'id', 'name'):
                    attr_dict[key] = 'rst-%s' % val
                elif key.lower() in ('classes', 'ids', 'names'):
                    attr_dict[key] = ['rst-%s' % cls for cls in val]
                elif key.lower() == 'href':
                    if attr_dict[key][:1]=='#':
                        attr_dict[key] = '#rst-%s' % attr_dict[key][1:]
                    else:
                        # If it's an external link, open it in a new
                        # page.
                        attr_dict['target'] = '_top'

        # For headings, use class="heading"
        if re.match(r'^h\d+$', tagname):
            attributes['class'] = ' '.join([attributes.get('class',''),
                                            'heading']).strip()

        return HTMLTranslator.starttag(self, node, tagname, suffix,
                                       **attributes)

    def visit_doctest_block(self, node):
        pysrc = node[0].astext()
        if node.get('codeblock'):
            self.body.append(HTMLDoctestColorizer().colorize_codeblock(pysrc))
        else:
            self.body.append(doctest_to_html(pysrc))
        raise SkipNode()

    def visit_emphasis(self, node):
        # Generate a corrent index term anchor
        if 'term' in node.get('classes') and node.children:
            doc = self.document.copy()
            doc[:] = [node.children[0].copy()]
            self.body.append(
                self._linker.translate_indexterm(ParsedRstDocstring(doc)))
            raise SkipNode()

        HTMLTranslator.visit_emphasis(self, node)

def python_code_directive(name, arguments, options, content, lineno,
                          content_offset, block_text, state, state_machine):
    """
    A custom restructuredtext directive which can be used to display
    syntax-highlighted Python code blocks.  This directive takes no
    arguments, and the body should contain only Python code.  This
    directive can be used instead of doctest blocks when it is
    inconvenient to list prompts on each line, or when you would
    prefer that the output not contain prompts (e.g., to make
    copy/paste easier).
    """
    text = '\n'.join(content)
    node = docutils.nodes.doctest_block(text, text, codeblock=True)
    return [ node ]

python_code_directive.arguments = (0, 0, 0)
python_code_directive.content = True

directives.register_directive('python', python_code_directive)

def term_role(name, rawtext, text, lineno, inliner,
            options={}, content=[]):

    text = docutils.utils.unescape(text)
    node = docutils.nodes.emphasis(rawtext, text, **options)
    node.attributes['classes'].append('term')

    return [node], []

roles.register_local_role('term', term_role)
