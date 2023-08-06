================
JTAC
================


.. image:: https://img.shields.io/pypi/v/jtac.svg
        :target: https://pypi.python.org/pypi/jtac

.. image:: https://img.shields.io/travis/corp-0/jtac.svg
        :target: https://travis-ci.org/corp-0/jtac

.. image:: https://readthedocs.org/projects/arma-serveradmin/badge/?version=latest
        :target: https://arma-serveradmin.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Start, stop and restart your arma servers just with cli


* Free software: MIT license
* Documentation: https://arma-serveradmin.readthedocs.io.

Installation
--------------
``pip install jtac``

Features
--------

* Use commands to start, stop, restart and change missions.

How to Use
----------
``jtac generate`` will create servers.json with all the parameters of your currently running servers,
so they can be used later. JTAC will try to operate your servers based on the port stored when you generated servers.json.

``jtac start <port>`` will find a server in servers.json that used that port and start a new server using its parameters.

``jtac kill <port>`` will stop a running server using the last PID registered with that port. Everytime you start a server with JTAC, JTAC will remeber the PID.

``jtac restart <port>`` will retart your server using the last parameters registered.

To Do
------
``jtac radio <command>`` a native way to remotely send commands to your server box.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
