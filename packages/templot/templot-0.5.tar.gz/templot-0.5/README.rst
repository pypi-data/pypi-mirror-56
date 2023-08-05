
.. image:: https://circleci.com/gh/khllkcm/templot/tree/master.svg?style=svg&circle-token=f6eb14760d058d82687c8c09cab77e407b2a67a5
    :target: https://circleci.com/gh/khllkcm/templot/tree/master
    
templot
=============

.. image:: ./doc/_static/logo.svg?raw=true&sanitize=true)
    :width: 50

Python package for visualizing evolution over time across geographical locations.

Contributing
=============


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

