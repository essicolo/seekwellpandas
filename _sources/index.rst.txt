Welcome to seekwellpandas's documentation!
=======================================

🐼🔬 Seek well, pandas! `seekwellpandas` (SQL-pandas) is a simple Python package that provides extensions to query pandas DataFrames using a SQL-like synthax.

Install
-------

You can install SeekwellPandas using pip:

.. code-block:: bash

    pip install seekwellpandas

Usage
-----

Here's a basic example of how to use SeekwellPandas:

.. code-block:: python

    import pandas as pd
    import seekwellpandas

    # Create a sample DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': ['a', 'b', 'a', 'b'],
        'C': [10, 20, 30, 40]
    })

    # Select columns
    result = df.select('A', 'B')

Features
--------

SeekwellPandas extends pandas DataFrames with SQL-like methods, including:

- ``select()``: Select specific columns
- ``where_()``: Filter rows based on a condition
- ``group_by()``: Group data by one or more columns
- ``order_by()``: Sort data
- ``join_()``: Join two DataFrames
- etc.

For more methods and detailed information on each method, please refer to the full documentation.

License
-------

This project is licensed under the GPLv3 License.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   _examples/basic-usage
