"""Support for a few things specific to documenting Twisted."""

from __future__ import print_function

from pydoctor import model, ast_pp, zopeinterface
from compiler import ast

from twisted.python.versions import Version
from twisted.python.deprecate import _getDeprecationWarningString

class TwistedModuleVisitor(zopeinterface.ZopeInterfaceModuleVisitor):

    def visitCallFunc_twisted_python_util_moduleMovedForSplit(self, funcName, node):
        # XXX this is rather fragile...
        origModuleName, newModuleName, moduleDesc, \
                        projectName, projectURL, globDict = node.args
        moduleDesc = ast_pp.pp(moduleDesc)[1:-1]
        projectName = ast_pp.pp(projectName)[1:-1]
        projectURL = ast_pp.pp(projectURL)[1:-1]
        modoc = """
%(moduleDesc)s

This module is DEPRECATED. It has been split off into a third party
package, Twisted %(projectName)s. Please see %(projectURL)s.

This is just a place-holder that imports from the third-party %(projectName)s
package for backwards compatibility. To use it, you need to install
that package.
""" % {'moduleDesc': moduleDesc,
       'projectName': projectName,
       'projectURL': projectURL}
        self.builder.current.docstring = modoc

    def visitClass(self, node):

        super(TwistedModuleVisitor, self).visitClass(node)

        cls = self.builder.current.contents[node.name]

        for a in list(cls.raw_decorators):
            if isinstance(a, ast.CallFunc):
                decorator = a.asList()
                fn = cls.expandName(decorator[0].name)
                if fn == "twisted.python.deprecate.deprecated":
                    cls._deprecated_info = deprecatedToUsefulText(cls.name, decorator)



def versionToUsefulText(version):

    return Version(*[x.value for x in version.asList()[1:] if x])


def deprecatedToUsefulText(name, deprecated):

    version = versionToUsefulText(deprecated[1])
    if deprecated[2]:
        if isinstance(deprecated[2], ast.Keyword):
            replacement = deprecated[2].asList()[1].value
        else:
            replacement = deprecated[2].value
    else:
        replacement = None

    return _getDeprecationWarningString(name, version, replacement=replacement) + "."


class TwistedFunction(zopeinterface.ZopeInterfaceFunction):

    def docsources(self):

        if self.decorators:
            for a in list(self.decorators):
                if isinstance(a, ast.CallFunc):
                    decorator = a.asList()
                    fn = self.expandName(decorator[0].name)
                    if fn == "twisted.python.deprecate.deprecated":
                        self._deprecated_info = deprecatedToUsefulText(self.name, decorator)

        for x in super(TwistedFunction, self).docsources():
            yield x


class TwistedASTBuilder(zopeinterface.ZopeInterfaceASTBuilder):
    ModuleVistor = TwistedModuleVisitor


class TwistedSystem(zopeinterface.ZopeInterfaceSystem):
    defaultBuilder = TwistedASTBuilder
    Function = TwistedFunction

    def privacyClass(self, obj):
        o = obj
        if o.fullName() == 'twisted.test':
            # Match this package exactly, so that proto_helpers
            # below is visible
            return model.PrivacyClass.VISIBLE
        while o:
            if o.fullName() == 'twisted.words.xish.yappsrt':
                return model.PrivacyClass.HIDDEN
            if o.fullName() == 'twisted.test.proto_helpers':
                return model.PrivacyClass.VISIBLE
            if isinstance(o, model.Package) and o.name == 'test':
                return model.PrivacyClass.HIDDEN
            o = o.parent
        return super(TwistedSystem, self).privacyClass(obj)
