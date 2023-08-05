=======================
Django Management Tools
=======================


.. image:: https://img.shields.io/pypi/v/django-management-tools.svg
        :target: https://pypi.python.org/pypi/django-management-tools

.. image:: https://img.shields.io/gitlab/pipeline/pennatus/django-management-tools/master
        :alt: Gitlab pipeline status

.. image:: https://readthedocs.org/projects/django-management-tools/badge/?version=latest
        :target: https://django-management-tools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Collection of tools to extend Django's manage.py command.


* Free software: MIT license
* Documentation: https://django-management-tools.readthedocs.io.


Features
--------

* `python manage.py createadmin --user <username> --password <password> --email <emailaddress>`
   username/password defaults to admin/admin
   email default to nothing


Installation
------------

Install ``django-management-tools`` from pip ::

    $ pip install django-vault-helpers

Add the new packages to your installed apps.

::

    INSTALLED_APPS = [
        ...
        'managementtools',
        ...
    ]





Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
