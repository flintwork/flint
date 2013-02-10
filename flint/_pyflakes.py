# -*- coding: utf-8 -*-
import pyflakes
import pyflakes.checker


def patch_pyflakes():
    """Add error codes to Pyflakes messages."""
    codes = dict([line.split()[::-1] for line in (
        'F401 UnusedImport',
        'F402 ImportShadowedByLoopVar',
        'F403 ImportStarUsed',
        'F404 LateFutureImport',
        'F810 Redefined',               # XXX Obsolete?
        'F811 RedefinedWhileUnused',
        'F812 RedefinedInListComp',
        'F821 UndefinedName',
        'F822 UndefinedExport',
        'F823 UndefinedLocal',
        'F831 DuplicateArgument',
        'F841 UnusedVariable',
    )])

    for name, obj in vars(pyflakes.messages).items():
        if name[0].isupper() and obj.message:
            obj.code = codes.get(name, 'F999')
patch_pyflakes()


class FlakesChecker(pyflakes.checker.Checker):
    """Subclass the Pyflakes checker to conform with the flint API."""
    name = 'pyflakes'
    version = pyflakes.__version__

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--builtins',
                          help="define more built-ins, comma separated")

    @classmethod
    def parse_options(cls, options):
        if options.builtins:
            cls.builtIns = cls.builtIns.union(options.builtins.split(','))

    def run(self):
        for m in self.messages:
            text = '%s %s' % (m.code, m.message) % m.message_args
            yield m.lineno, 0, text, type(m)
