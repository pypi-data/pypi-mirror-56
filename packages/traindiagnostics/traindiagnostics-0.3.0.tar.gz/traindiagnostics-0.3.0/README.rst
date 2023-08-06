.. |travis| image:: https://travis-ci.com/gjeusel/ticts.svg?branch=master
   :target: https://travis-ci.com/gjeusel/ticts

.. |readthedocs| image:: https://readthedocs.org/projects/ticts/badge/?version=latest
   :target: http://ticts.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |codecov| image:: https://codecov.io/gh/gjeusel/ticts/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/gjeusel/ticts

.. |pypi| image:: https://badge.fury.io/py/ticts.svg
   :target: https://pypi.python.org/pypi/traindiagnostics/
   :alt: Pypi package

.. |python| image:: https://img.shields.io/pypi/pyversions/traindiagnostics
   :target: https://www.python.org/downloads/release/python-360/
   :alt: PyPI - Python Version

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black

.. |license| image:: https://img.shields.io/pypi/l/traindiagnostics?color=purple
   :target: https://github.com/timolesterhuis/traindiagnostics/blob/master/LICENSE
   :alt: PyPI - License

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/timolesterhuis/traindiagnostics/master?filepath=example.ipynb
   :alt: Launch Binder

================
traindiagnostics
================
|python| |pypi| |license| |black| |binder|

A Python library for unevenly-spaced time series analysis in train diagnostics.
Build on top of the magnificent `ticts <https://github.com/gjeusel/ticts>`_ library.

Installation
------------

.. code:: bash

    pip install traindiagnostics

Want to try it out first without installing? With `binder <https://mybinder.org/v2/gh/timolesterhuis/traindiagnostics/master?filepath=example.ipynb>`_
you can test out the code in an online jupyter notebook.

Usage
-----

.. code:: python

    import traindiagnostics as td
    ts = td.TimeSeries({
        '2019-01-01 09:00:00': 0,
        '2019-01-01 09:00:05': 1,
        '2019-01-01 09:01:02': 0,
        '2019-01-01 09:05:09': 1,
        '2019-01-01 09:05:16': 0,
        '2019-01-01 09:11:01': 1,
        '2019-01-01 09:12:59': 0,
    })

   not_in_index = '2019-01-01 00:05:00'
   assert ts[not_in_index] == 1  # step function, previous value

   ts['2019-01-01 00:04:00'] = 10
   assert ts[not_in_index] == 10

   assert ts + ts == 2 * ts

   ts_evenly_spaced = ts.sample(freq='1Min')

   # From ticts to pandas, and the other way around
   assert ts.equals(
      ts.to_dataframe().to_ticts(),
   )

Contributing
------------

Missing some features? create an issue or pull request!
