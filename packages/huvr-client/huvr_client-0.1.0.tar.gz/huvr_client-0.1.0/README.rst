HUVR Client
=========================================================

A Python client (with examples) to connect to HUVRdata.

Features
--------

* a Python client library for the HUVRdata application


Setup Credentials
-----------------

Set up your credentials file

.. code-block:: bash

    $ mkdir ~/.huvr_api_client
    $ cp huvrdatacloud_credentials.json ~/.huvr_api_client


Then edit the :code:`~/.huvr_api_client` file and add your login information.


Run Through the Examples
------------------------

You are now ready to run through our examples.
Edit this file :code:`API_Client_Example.py` where you will modify 2 vars.
Go to the :code:`__main__` section of the code and change the :code:`subdomain` to the desired
subdomain to run on, and change the :code:`running_in` variable to which ever environment you want to test on.

Finally: Uncomment the :code:`profiles_example()` section.
Now run it:

.. code-block:: bash

    $ ./API_Client_Example.py



Using Lint in the development env.
----------------------------------
You can use flake8 to lent your python code as you are developing. Note: when checking in code the google builder
also lents the python code.

.. code-block:: bash

    $ make lint



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
This library uses the python `Requests <http://python-requests.org>`_ Library.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
