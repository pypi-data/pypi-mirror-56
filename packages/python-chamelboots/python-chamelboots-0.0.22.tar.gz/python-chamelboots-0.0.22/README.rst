========
Overview
========


Version v0.0.22.
----------------


This is a proof of concept package. It came out of working with the `Nikolo static site generator`_.

While it's more convenient to write pages and posts with Markdown or reStructuredText_, sometimes HTML is more precise, especially regarding custom `Bootstrap components`_. The issue is that writing HTML by hand is tedious and error-prone. Template libraries do help, but they introduce their own clumsy syntax into HTML. Except at least one: Chameleon_.

Then there is the issue of learning the `template attribute language`_ (TAL) in Chameleon templates.. Fortunately, TAL only has 10 statements. 

This library address the issue of building validated Chameleon templates that when rendered produce validated HTML programmatically_.

The specification is to easily create Chameleon templates to output HTML using strings and Python code.

See working—and constantly changing—examples at `this blog post`_ and `at this blog post`_ .

Reiterating over these posts helps me strategize ways of making the creation of HTML using Python more efficient.

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-chamelboots/badge/?style=flat
    :target: https://readthedocs.org/projects/python-chamelboots
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/dm-wyncode/python-chamelboots.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/dm-wyncode/python-chamelboots

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/dm-wyncode/python-chamelboots?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/dm-wyncode/python-chamelboots

.. |requires| image:: https://requires.io/github/dm-wyncode/python-chamelboots/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/dm-wyncode/python-chamelboots/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/dm-wyncode/python-chamelboots/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/dm-wyncode/python-chamelboots

.. |version| image:: https://img.shields.io/pypi/v/chamelboots.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/chamelboots

.. |wheel| image:: https://img.shields.io/pypi/wheel/chamelboots.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/chamelboots

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/chamelboots.svg
    :alt: Supported versions
    :target: https://pypi.org/project/chamelboots

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/chamelboots.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/chamelboots

.. |commits-since| image:: https://img.shields.io/github/commits-since/dm-wyncode/python-chamelboots/v0.0.6.svg
    :alt: Commits since latest release
    :target: https://github.com/dm-wyncode/python-chamelboots/compare/v0.0.6...master



.. end-badges


Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

.. code-block:: bash

    pip install chamelboots

You can also install the in-development version with

.. code-block:: bash

    pip install https://github.com/dm-wyncode/python-chamelboots/archive/master.zip


It is still possible to install by cloning this repository, activating a virtual environment, and running the following:

.. code-block:: bash

   python setup.py install 



Documentation
=============


https://python-chamelboots.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

.. _`Nikolo static site generator`: https://getnikola.com/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _`Bootstrap components`: https://getbootstrap.com/docs/4.3/components/alerts/
.. _Chameleon: https://chameleon.readthedocs.io/en/latest/
.. _`template attribute language`: https://chameleon.readthedocs.io/en/latest/reference.html#basics-tal
.. _programmatically: https://english.stackexchange.com/a/12246/159162
.. _`this blog post`: https://zip.apps.selfip.com/posts/create-html-with-strings-and-dictionaries-in-python/
.. _`Python Packages index`: https://pypi.org/
.. _`at this blog post`: https://zip.apps.selfip.com/posts/create-table-of-all-bootstrap-classes/
