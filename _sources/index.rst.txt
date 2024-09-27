Welcome to seekwellpandas's documentation!
=======================================

🐼🔬 Seek well, pandas! `seekwellpandas` (SQL-pandas) is a simple Python package that provides extensions to query pandas DataFrames using a SQL-like synthax.

Install
-------

`pip install seekwellpandas`.


Usage
-----

```python
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
```


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   _examples/basic-usage
