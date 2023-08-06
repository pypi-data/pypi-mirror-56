========
Overview
========

improved representation of Python complex numbers

* Free software: BSD 2-Clause License

Installation
============

::

    pip install ccomplex

You can also install the in-development version with::

    pip install git+ssh://git@https://github.com/urbanij/ccomplex/urbanij/python-ccomplex.git@master

Documentation
=============


https://python-ccomplex.readthedocs.io/


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
