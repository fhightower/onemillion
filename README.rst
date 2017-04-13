===============================
onemillion
===============================


.. image:: https://img.shields.io/pypi/v/onemillion.svg
        :target: https://pypi.python.org/pypi/onemillion

.. image:: https://img.shields.io/travis/fhightower/onemillion.svg
        :target: https://travis-ci.org/fhightower/onemillion

.. image:: https://codecov.io/gh/fhightower/onemillion/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/fhightower/onemillion

.. image:: https://readthedocs.org/projects/onemillion/badge/?version=latest
        :target: https://onemillion.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/fhightower/onemillion/shield.svg
     :target: https://pyup.io/repos/github/fhightower/onemillion/
     :alt: Updates

.. image:: https://www.quantifiedcode.com/api/v1/project/901a226d41ef48c08696b0c16583149b/badge.svg
  :target: https://www.quantifiedcode.com/app/project/901a226d41ef48c08696b0c16583149b
  :alt: Code issues

Determine if a domain is in the Alexa or Cisco top one million domain list. This can be used, to some extent, as a whitelist or reputation check for suspicious domains.

* Documentation: https://onemillion.readthedocs.io.


Installation
============

The recommended means of installation is using `pip <https://pypi.python.org/pypi/pip/>`_:

``pip install onemillion``

Alternatively, you can install onemillion as follows:

.. code-block:: shell

    git clone https://github.com/fhightower/onemillion.git && cd onemillion;
    python setup.py install --user;

Usage
=====

Default Usage
-------------

The default usage of onemillion is as follows:

.. code-block:: python

    from onemillion import onemillion

    o = onemillion.OneMillion()
    o.domain_in_million("google.com")  # True
    o.domain_in_million("gaagle.com")  # False

Using the method described above, the alexa and cisco top one million domain lists as well as a bit of metadata will be stored in the home directory: ``~/.onemillion``.

No Caching
----------

If you do not want to cache the domain lists, you can tell onemillion not cache anything by setting ``cache=False`` on initialization as demonstrated below:

.. code-block:: python

    from onemillion import onemillion

    # do not cache anything
    o = onemillion.OneMillion(cache=False)
    o.domain_in_million("google.com")  # True
    o.domain_in_million("gaagle.com")  # False

The code described above is fine if you are only making one or two calls or if storage space is a concern, but it is suggested that you cache the lists if feasible so as to limit traffic to the domain lists.

**NOTE:** currently, the 'No caching' configuration will throw an error. This will be updated and handled when `issue #12 <https://github.com/fhightower/onemillion/issues/12>`_ is fixed.

Custom Cache Location
---------------------

If you are caching the lists but want to cache them somewhere other than your home directory, you can specify a custom cache location by setting the ``cache_location`` parameter when initializing onemillion as demonstrated below:

.. code-block:: python

    from onemillion import onemillion

    # cache data to a specific path
    o = onemillion.OneMillion(cache_location=<YOUR_PATH_HERE>)
    o.domain_in_million("google.com")  # True
    o.domain_in_million("gaagle.com")  # False

This will cache the domain lists in the path you provide.

No Update
---------

If you have already run onemillion and have the domain lists cached, but do not want to keep updating them, you can specify ``update=False`` on initialization as demonstrated below:

.. code-block:: python

    from onemillion import onemillion

    # do not update cached content
    o = onemillion.OneMillion(update=False)
    o.domain_in_million("google.com")  # True
    o.domain_in_million("gaagle.com")  # False

Be aware that, by default, onemillion will check to see if it has already updated the domain lists today before even trying to update them. In other words, onemillion handles updating responsibly and intelligently by default and there are few cases in which this configuration (using ``update=False``) is necessary. Nevertheless... it's there and you are welcome to use it.

Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

