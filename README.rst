====================
Pinned Import Linter
====================

.. image:: https://img.shields.io/pypi/v/pinned-import-linter.svg
    :target: https://pypi.org/project/pinned-import-linter

.. image:: https://img.shields.io/pypi/pyversions/pinned-import-linter.svg
    :alt: Python versions
    :target: https://pypi.org/project/pinned-import-linter/

.. image:: https://github.com/maintainer64/pinned-import-linter/workflows/CI/badge.svg?branch=main
     :target: https://github.com/maintainer64/pinned-import-linter/actions?workflow=CI
     :alt: CI Status

⚡ A plugin for python that will help you standardize imports from any libraries.

* Free software: MIT License

Overview
--------

Pinned Import Lint is a command-line utility that allows users to verify whether they
are adhering to the established syntax for importing modules in their Python projects.
This is done by checking the permissible names for modules, packages, and their importation rules,
as specified in a configuration file.

The configuration file lists the modules to monitor
and provides settings for each module, such as the ``allow_from`` option,
which restricts the import of submodules from packages using the ``from`` keyword.
Only selected packages can be imported through a common name or alias.

Pinned Import lint helps maintain consistency in the way modules are imported,
enforcing a uniform style of importing packages in Python.

It draws inspiration from similar projects, such as:

1. https://github.com/seddonym/import-lint
2. https://github.com/adamchainz/flake8-tidy-import

Quick start
-----------

Install Pinned Import Linter::


    pip install pinned-import-linter

Select libraries and what import styles are available for them.
In this example, we show the standard configuration for importing libraries into Python.

Create a ``tox.ini`` file in your project or any other file
(then it will need to be connected via the ``--config`` parameter in the *CLI*)
with similar contents:

.. code-block:: ini

    [pinned_import_linter]
    package_names = typing,itertools,datetime,sys,pathlib

    [pinned_import_linter.typing]
    allow_alias = true
    alias_names = t
    allow_from = false
    allow_package = false

    [pinned_import_linter.itertools]
    allow_alias = true
    alias_names = it
    allow_from = false
    allow_package = false

    [pinned_import_linter.datetime]
    allow_alias = true
    alias_names = dt
    allow_from = false
    allow_package = false

    [pinned_import_linter.sys]
    allow_alias = false
    allow_from = false
    allow_package = true

    [pinned_import_linter.pathlib]
    allow_alias = false
    allow_from = true
    allow_package = false

In the ``[pinned_import_linter]`` section, there is only one parameter expected, ``package_name``.
These are the libraries whose import styles will be restricted in the subsequent sections.

1. For the ``typing``, ``itertools``, and ``datetime`` libraries, we have specified the ``allow_alias`` parameter.
This allows for the use of alias imports while prohibiting the usage of the `from` statement.
We accomplish this by setting ``allow_from = false`` and disallowing
imports without an alias by setting ``allow_package = false``.

To define allowed names (if none are defined, all names are allowed), we use the ``alias_names = t,tu,tp,tv`` parameter, separated by commas.
Therefore, only the specified packages will be permitted to be imported via alias from this list.

2. For the ``sys`` standard library set ``allow_package = true`` and
the rest to ``false`` in order to import a package using the
keyword ``from`` or alias a name (``import sys as ...``)
becomes unavailable.

3. For the ``pathlib`` standard library set ``allow_from = true`` and
the rest to ``false`` in order to allow importing only through the ``from`` keyword.

4. For the other Libraries (not described) in
the configuration can be imported in any way.


Now, from your project root, run::


    lint-pinned-imports --config tox.ini main.py

For a file with this configuration:

.. code-block:: python

    from typing import Callable, List
    from itertools import product
    import itertools
    import pathlib as pt
    from os import linesep

Output after CLI execution:

.. code-block:: text

    main.py:1: error: Banned import 'from typing import ...'
    main.py:2: error: Banned import 'from itertools import ...'
    main.py:3: error: Banned import 'import itertools'
    main.py:4: error: Banned import 'import pathlib as ...'

Connect all files on pre-commit
-------------------------------

1. Add package on dev-dependency in your project on Python
2. Add step into your .pre-commit-config.yaml

.. code-block:: yml

    repos:
      - repo: local
        hooks:
          - id: lint-pinned-imports
            name: Restricted imports
            entry: lint-pinned-imports --config tox.ini
            language: system
            files: \.py$
            pass_filenames: true
