===============================
onemillion
===============================

.. image:: https://api.codacy.com/project/badge/Grade/e47d712af7e24ac493e76392d1613e82
   :alt: Codacy Badge
   :target: https://www.codacy.com/app/fhightower/onemillion?utm_source=github.com&utm_medium=referral&utm_content=fhightower/onemillion&utm_campaign=badger


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

Determine if a domain is in the Alexa or Cisco top one million domain list.

Documentation is available here: `https://onemillion.readthedocs.io <https://onemillion.readthedocs.io>`_ .

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

When using the default settings, the following steps will be taken when an instance of onemillion is initialized and the ``domain_in_million`` function called:

1. Check to see if the domain lists have been updated today.
2a. If they have been updated today, look for the given domain in the lists and stop.
2b. If the lists have not been updated today, make a ``HEAD`` request and check the current etag against the previous etag (stored locally) to see if the lists have been updated.
3a. If the etags are the same (meaning the lists have not been updated), look for the given domain in the lists and stop.
3b. If the etags are different (meaning the lists have been updated), make a request for the lists, unzip them, and save them in the default cache location (``~/.onemillion``).
4. Now that the lists are updated, search for the given domain in the lists.

Default Usage ~ Hello World!
----------------------------

The default usage of onemillion is as follows:

.. code-block:: python

    from onemillion import onemillion

    o = onemillion.OneMillion()
    o.domain_in_million("google.com")  # 1
    o.domain_in_million("gaagle.com")  # None

Using the method described above, the alexa and cisco top one million domain lists as well as a bit of metadata will be stored in the home directory: ``~/.onemillion``.

No Caching
----------

If you do not want to cache the domain lists, you can tell onemillion not cache anything by setting ``cache=False`` on initialization as demonstrated below:

.. code-block:: python

    from onemillion import onemillion

    # do not cache anything
    o = onemillion.OneMillion(cache=False)
    o.domain_in_million("google.com")  # 1
    o.domain_in_million("gaagle.com")  # None

The code described above is fine if you are only making one or two calls or if storage space is a concern, but it is suggested that you cache the lists if feasible so as to limit traffic to the domain lists.

**NOTE:** currently, the 'No caching' configuration will throw an error. This will be updated and handled when `issue #12 <https://github.com/fhightower/onemillion/issues/12>`_ is fixed.

Custom Cache Location
---------------------

If you are caching the lists but want to cache them somewhere other than your home directory, you can specify a custom cache location by setting the ``cache_location`` parameter when initializing onemillion as demonstrated below:

.. code-block:: python

    from onemillion import onemillion

    # cache data to a specific path
    o = onemillion.OneMillion(cache_location=<YOUR_PATH_HERE>)
    o.domain_in_million("google.com")  # 1
    o.domain_in_million("gaagle.com")  # None

This will cache the domain lists in the path you provide.

No Update
---------

If you have already run onemillion and have the domain lists cached, but do not want to keep updating them, you can specify ``update=False`` on initialization as demonstrated below:

.. code-block:: python

    from onemillion import onemillion

    # do not update cached content
    o = onemillion.OneMillion(update=False)
    o.domain_in_million("google.com")  # 1
    o.domain_in_million("gaagle.com")  # None

Be aware that onemillion will, by default, check to see if it has already updated the domain lists today before making any requests. Thus, onemillion handles updating responsibly and intelligently by default and there are few cases in which this configuration (using ``update=False``) is necessary. Nevertheless... it's there and you are welcome to use it.

Credits
=======

This package was created with Cookiecutter_ and the `fhightower/python-project-template`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`fhightower/python-project-template`: https://github.com/fhightower/python-project-template
