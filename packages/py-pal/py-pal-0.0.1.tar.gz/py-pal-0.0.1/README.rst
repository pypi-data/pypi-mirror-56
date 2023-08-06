========
Overview
========

.. start-badges

|version| |wheel| |supported-versions| |supported-implementations|

.. |version| image:: https://img.shields.io/pypi/v/py-pal.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/py-pal

.. |wheel| image:: https://img.shields.io/pypi/wheel/py-pal.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/py-pal

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/py-pal.svg
    :alt: Supported versions
    :target: https://pypi.org/project/py-pal

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/py-pal.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/py-pal

.. end-badges

Python Performance Analysis Library or py-pal is a bytecode profiling toolkit.

Installation
============

This project requires CPython to run.
Install Python >= 3.7, then install py-pal by running:

    pip install py-pal

Documentation
=============
TBA


Overview
========

Calling py-pal as module with

    python -m py_pal file.py

or

    pypal file.py

Measure specific functions using the decorator:

.. sourcecode:: python

    from py_pal.core import profile

    @profile
    def test():
        pass


Using the context manager:

.. sourcecode:: python

    from py_pal.tracer import Tracer

    with Tracer() as t:
        pass

Using the API:

.. sourcecode:: python

    from py_pal.estimator import ComplexityEstimator
    from py_pal.tracer import Tracer


    t = Tracer()
    t.trace()

    # Your function
    pass

    t.stop()
    estimator = ComplexityEstimator(t)
    res = estimator.export()

    # Do something with the resulting DataFrame
    print(res)


Modes
-----
Profiling and Performance Testing

Tracing processes
-----------------


Development
===========

To run the all tests run:


    pip install -r dev-requirements.txt
    pytest tests

FAQ
===

Why not use a standard profiler?
--------------------------------

Using absolute timing data vs synthetic timing data using opcodes.
