
.. image:: https://circleci.com/gh/khllkcm/templot/tree/master.svg?style=svg&circle-token=f6eb14760d058d82687c8c09cab77e407b2a67a5
    :target: https://circleci.com/gh/khllkcm/templot/tree/master
    
templot
=============

.. image:: ./doc/_static/logo.svg?raw=true&sanitize=true)
    :width: 50

Simple template to package plotting functions. Material for teaching
`ensae_teaching_cs <https://github.com/sdpython/ensae_teaching_cs>`_.
It implements basic CI and documentation. One example of use:
`plot_aggregated_map.py
<https://github.com/khllkcm/templot/blob/master/examples/plot_aggregated_map.py>`_.

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

    python -m flake8 templot tests examples
