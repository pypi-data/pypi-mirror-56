=============================
django-vadmin
=============================

.. image:: https://badge.fury.io/py/django-vadmin.svg
    :target: https://badge.fury.io/py/django-vadmin

.. image:: https://travis-ci.org/bushig/django-vadmin.svg?branch=master
    :target: https://travis-ci.org/bushig/django-vadmin

.. image:: https://codecov.io/gh/bushig/django-vadmin/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bushig/django-vadmin

Your project description goes here

Documentation
-------------

The full documentation is at https://django-vadmin.readthedocs.io.

Quickstart
----------

Install django-vadmin::

    pip install django-vadmin

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'vadmin',
        ...
    )

Add django-vadmin's URL patterns:

.. code-block:: python

    from vadmin import urls as vadmin_urls


    urlpatterns = [
        ...
        url(r'^', include(vadmin_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
