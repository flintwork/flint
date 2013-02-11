# -*- coding: utf-8 -*-
import os
import sys

import pep8

from flint.util import OrderedSet

__version__ = '0.2a0'
if sys.platform == 'win32':
    DEFAULT_CONFIG = os.path.expanduser(r'~\.flint')
else:
    DEFAULT_CONFIG = os.path.join(os.getenv('XDG_CONFIG_HOME') or
                                  os.path.expanduser('~/.config'), 'flint')


def register_extensions():
    """Register all the extensions."""
    extensions = OrderedSet()
    extensions.add(('pep8', pep8.__version__))
    parser_hooks = []
    options_hooks = []
    try:
        from pkg_resources import iter_entry_points
    except ImportError:
        pass
    else:
        for entry in iter_entry_points('flint.extension'):
            checker = entry.load()
            pep8.register_check(checker, codes=[entry.name])
            extensions.add((checker.name, checker.version))
            if hasattr(checker, 'add_options'):
                parser_hooks.append(checker.add_options)
            if hasattr(checker, 'parse_options'):
                options_hooks.append(checker.parse_options)
    return extensions, parser_hooks, options_hooks


def get_parser():
    (extensions, parser_hooks, options_hooks) = register_extensions()
    details = ', '.join(['%s: %s' % ext for ext in extensions])
    parser = pep8.get_parser('flint', '%s (%s)' % (__version__, details))
    for opt in ('--repeat', '--testsuite', '--doctest'):
        try:
            parser.remove_option(opt)
        except ValueError:
            pass
    parser.add_option('--exit-zero', action='store_true',
                      help="exit with code 0 even if there are errors")
    for parser_hook in parser_hooks:
        parser_hook(parser)
    return parser, options_hooks


def main():
    """Parse options and run checks on Python source."""
    # Prepare
    parser, options_hooks = get_parser()
    flint_style = pep8.StyleGuide(
        parse_argv=True, config_file=DEFAULT_CONFIG, parser=parser)
    options = flint_style.options
    for options_hook in options_hooks:
        options_hook(options)

    # Run the checkers
    report = flint_style.check_files()

    # Print the final report
    if options.statistics:
        report.print_statistics()
    if options.benchmark:
        report.print_benchmark()
    if report.total_errors:
        if options.count:
            sys.stderr.write(str(report.total_errors) + '\n')
        if not options.exit_zero:
            sys.exit(1)

if __name__ == '__main__':
    main()
