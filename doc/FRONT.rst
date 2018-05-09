.. This file is a part of the AnyBlok / JsonSchema project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.


.. contents::

Front Matter
============

Information about the AnyBlok / JsonSchema project.

Project Homepage
----------------

AnyBlok / JsonSchema is hosted on `github <http://github.com>`_ - the main project
page is at http://github.com/AnyBlok/anyblok_jsonschema. Source code is tracked here
using `GIT <https://git-scm.com>`_.

Releases and project status are available on Pypi at 
http://pypi.python.org/pypi/anyblok_jsonschema.

The most recent published version of this documentation should be at
http://doc.anyblok_jsonschema.anyblok.org.

Installation
------------

Install released versions of AnyBlok from the Python package index with 
`pip <http://pypi.python.org/pypi/pip>`_ or a similar tool::

    pip install anyblok_jsonschema

Installation via source distribution is via the ``setup.py`` script::

    python setup.py install

Installation will add the ``anyblok`` commands to the environment.

.. note:: AnyBlok use Python version >= 3.3

Running Tests
-------------

.. seealso:: the :ref:`section about testing of AnyBlok applications
             <basedoc_tests>`.


To run framework tests with ``nose``::

    pip install nose
    nosetests anyblok_jsonschema/tests

AnyBlok is tested continuously using `Travis CI
<https://travis-ci.org/AnyBlok/anyblok_jsonschema>`_


Contributing (hackers needed!)
------------------------------

Anyblok is at a very early stage, feel free to fork, talk with core dev, and spread the word!

Author
------

Jean-Sébastien Suzanne

Contributors
------------

`Anybox <http://anybox.fr>`_ team:

* Jean-Sébastien Suzanne

other:

* Franck Bret

Bugs
----

Bugs and feature enhancements to AnyBlok should be reported on the `Issue 
tracker <https://github.com/AnyBlok/anyblok_jsonschema/issues>`_.
