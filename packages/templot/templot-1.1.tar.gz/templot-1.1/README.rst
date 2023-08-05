templot
=============

.. image:: ./doc/_static/logo.svg?raw=true&sanitize=true)
    :width: 50

Python package for visualizing evolution over time across geographical locations.

Contributing
=============

Install the dependencies in ``requirements.txt`` and ``requirements-dev.txt``.

Generate the setup in subfolder ``dist``:

::

    python setup.py sdist

Generate the documentation in folder ``dist/html``:

::

    python -m sphinx -T -b html doc dist/html

Run the unit tests:

::

    python -m unittest discover tests

    
To check style:

::

    python -m flake8 templot tests examples --ignore=E501,W503

