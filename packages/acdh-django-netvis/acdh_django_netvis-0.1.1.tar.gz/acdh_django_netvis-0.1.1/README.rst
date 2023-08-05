=============================
acdh-django-netvis
=============================

.. image:: https://badge.fury.io/py/acdh_django_netvis.svg
    :target: https://badge.fury.io/py/acdh_django_netvis

.. image:: https://travis-ci.org/csae8092/acdh_django_netvis.svg?branch=master
    :target: https://travis-ci.org/csae8092/acdh_django_netvis

.. image:: https://codecov.io/gh/csae8092/acdh_django_netvis/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/csae8092/acdh_django_netvis

App to visualize model objects as network graph

Documentation
-------------

The full documentation is at https://acdh_django_netvis.readthedocs.io.

Quickstart
----------

Install acdh-django-netvis::

    pip install acdh_django_netvis

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'netvis',
        ...
    )

Add acdh-django-netvis's URL patterns:

.. code-block:: python


    urlpatterns = [
        ...
        url(r'^netvis/', include('netvis.urls', namespace="netvis")),
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
