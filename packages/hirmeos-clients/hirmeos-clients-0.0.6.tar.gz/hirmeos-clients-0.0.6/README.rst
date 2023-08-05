HIRMEOS Clients
===============

Python clients for interacting with APIs that were developed as part of the
HIRMEOS project.

Once this has been shown to be working properly, and able to integrate with the
HIRMEOS drivers it can be moved to a HIRMEOS/OPERAS PyPI Repo.


Until CI is ready
-----------------
  .. code-block:: bash

    $ python3 setup.py sdist bdist_wheel
    $ twine upload dist/*.tar.gz
