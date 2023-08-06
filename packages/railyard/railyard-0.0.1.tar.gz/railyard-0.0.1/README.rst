railyard
========

Local application development server
------------------------------------

Features
========
* Basic compatibility with Google App Engine `app.yaml <https://cloud.google.com/appengine/docs/standard/python3/config/appref>`_ files
* Basic compatibility with Google App Engine `dispatch.yaml <https://cloud.google.com/appengine/docs/standard/python3/reference/dispatch-yaml>`_ files
* Support for static files

Use
===

To run an application defined in a :code:`app.yaml` file::

  $ railyard app.yaml

To run an application which uses a :code:`dispatch.yaml` file::

  $ railyard dispatch.yaml

Railyard will first search the folder it is run from for the service definition files, failing that, it will search folders matching the service names. For example, take the following :code:`dispatch.yaml`::

  dispatch:
    - url: "*/app1/*"
      service: app1

    - url: "*/app2/*"
      service: app2

Railyard will use files in the following order:

* :code:`./app1.yaml`
* :code:`./app1/app1.yaml`
* :code:`./app2.yaml`
* :code:`./app2/app2.yaml`

Development
===========

Setup
-----

It is recommended to develop using a `pipenv <https://pipenv.kennethreitz.org/en/latest/>`_.

A development environment can be set up automatically::

  $ pipenv install --dev

You can work directly inside the development environment::

  $ pipenv shell

From inside the development environment, you can install the pre-commit hooks using `pre-commit <https://pre-commit.com/>`_::

  $ pre-commit install

To run the pre-commit hooks manually::

  $ pre-commit run --all-files

Tests
-----

To run the unit tests::

  $ python -m unittest

The pre-commit tests are run using `coverage <https://coverage.readthedocs.io/>`_. To see where the coverage tests are failing::

  $ coverage report -m
