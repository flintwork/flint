flint - the modular Python source code checker
==============================================

Flint is a thin wrapper around some Python checkers.

.. note::
   ``flint`` is now merged into `Flake8 2.0
   <https://pypi.python.org/pypi/flake8>`_.
   Please consider https://pypi.python.org/pypi/flake8 instead.

----


Features
--------

* Based on the ``pep8`` and the ``pyflakes`` checkers.

* Easy to configure, with unified output.

* Extendable through ``flint.extension`` entry points.

* Plugin examples:
  `flint-mccabe <https://github.com/flintwork/flint-mccabe>`_ and
  `pep8-naming <https://github.com/flintwork/pep8-naming>`_


Installation
------------

You can install, upgrade, uninstall ``flint`` with these commands::

  $ pip install flint
  $ pip install --upgrade flint
  $ pip uninstall flint


Usage and output
----------------

Flint runs all the registered checkers with a single ``flint`` script.
It accepts the same options as the ``pep8`` tool and additional options
for the plugins.  The output merges the errors from all the tools.

Example (with McCabe plugin)::

  $ flint --version
  0.1 (pep8: 1.4.2, pyflakes: 0.6.1, mccabe: 0.1)
  $
  $ flint --first --max-complexity 10 optparse.py
  optparse.py:61:11: E401 multiple imports on one line
  optparse.py:65:1: E302 expected 2 blank lines, found 1
  optparse.py:235:34: W602 deprecated form of raising exception
  optparse.py:265:5: E303 too many blank lines (2)
  optparse.py:375:31: E211 whitespace before '('
  optparse.py:404:17: E201 whitespace after '{'
  optparse.py:404:23: E203 whitespace before ':'
  optparse.py:407:53: E202 whitespace before '}'
  optparse.py:530:20: E124 closing bracket does not match visual indentation
  optparse.py:597:21: W601 .has_key() is deprecated, use 'in'
  optparse.py:637:34: E721 do not compare types, use 'isinstance()'
  optparse.py:639:80: E501 line too long (81 > 79 characters)
  optparse.py:700:17: E125 continuation line does not distinguish itself from next logical line
  optparse.py:1387:1: F841 local variable 'stop' is assigned to but never used
  optparse.py:1504:1: C901 'OptionParser._process_short_opts' is too complex (10)
  $


Configuration
-------------

The behaviour may be configured at two levels.

The user settings are read from the ``~/.config/flint`` file.
Example::

  [flint]
  ignore = E226,E302,E41
  max-line-length = 160

At the project level, a ``tox.ini`` file or a ``setup.cfg`` file is read
if present.  Only the first file is considered.  If this file does not
have a ``[flint]`` section, no project specific configuration is loaded.

If the ``ignore`` option is not in the configuration and not in the arguments,
only the error codes ``E226`` and ``E241/E242`` are ignored (see below).


Message codes
-------------

The convention of Flint is to assign a code to each error or warning, like
the ``pep8`` tool.  These codes are used to configure the list of errors
which are selected or ignored.

Each code consists of an upper case ASCII letter followed by three digits.
The recommendation is to use a different prefix for each plugin.

A list of the known prefixes is published below:

- ``E***``/``W***``: `pep8 errors and warnings
  <http://pep8.readthedocs.org/en/latest/intro.html#error-codes>`_
- ``F***``: PyFlakes codes (see below)
- ``C9**``: McCabe complexity plugin `flint-mccabe
  <https://github.com/flintwork/flint-mccabe>`_
- ``N8**``: Naming Conventions plugin `pep8-naming
  <https://github.com/flintwork/pep8-naming>`_


The original PyFlakes does not provide error codes.  Flint patches the PyFlakes
messages to add the following codes:

+------+--------------------------------------------------------------------+
| code | sample message                                                     |
+======+====================================================================+
| F401 | ``module`` imported but unused                                     |
+------+--------------------------------------------------------------------+
| F402 | import ``module`` from line ``N`` shadowed by loop variable        |
+------+--------------------------------------------------------------------+
| F403 | 'from ``module`` import \*' used; unable to detect undefined names |
+------+--------------------------------------------------------------------+
| F404 | future import(s) ``name`` after other statements                   |
+------+--------------------------------------------------------------------+
+------+--------------------------------------------------------------------+
| F811 | redefinition of unused ``name`` from line ``N``                    |
+------+--------------------------------------------------------------------+
| F812 | list comprehension redefines ``name`` from line ``N``              |
+------+--------------------------------------------------------------------+
| F821 | undefined name ``name``                                            |
+------+--------------------------------------------------------------------+
| F822 | undefined name ``name`` in __all__                                 |
+------+--------------------------------------------------------------------+
| F823 | local variable ``name`` ... referenced before assignment           |
+------+--------------------------------------------------------------------+
| F831 | duplicate argument ``name`` in function definition                 |
+------+--------------------------------------------------------------------+
| F841 | local variable ``name`` is assigned to but never used              |
+------+--------------------------------------------------------------------+


Original projects
-----------------

Thank you to the authors of the various projects which are the building blocks
of Flint:

- pep8: https://github.com/jcrocholl/pep8
- pyflakes: https://launchpad.net/pyflakes
- flake8: https://bitbucket.org/tarek/flake8


Links
-----

* `pep8 documentation <http://pep8.readthedocs.org/>`_

* `flake8 documentation <https://flake8.readthedocs.org>`_

* `flint on GitHub <http://github.com/flintwork/flint>`_
