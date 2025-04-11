# Seek well, pandas

`seekwellpandas` (SQL-pandas) is a pandas extension that provides SQL-inspired methods to manipulate DataFrames in a more intuitive way, closely resembling SQL syntax.

## Features

`seekwellpandas` adds several SQL methods to your pandas DataFrames, among them:

- `SELECT()`: Select specific columns, including negative selection.
- `WHERE()`: Filter rows based on a condition.
- `GROUP_BY()`: Group data by one or more columns.
- `HAVING()`: Filter groups based on a condition.
- `ORDER_BY()`: Sort data by one or more columns.
- `LIMIT()`: Limit the number of returned rows.
- `JOIN()`: Join two DataFrames.
- `UNION()`: Union two DataFrames.
- `DISTINCT()`: Remove duplicates.
- `INTERSECT()`: Find the intersection between two DataFrames.
- `DIFFERENCE()`: Find the difference between two DataFrames.
- `ADD_COLUMN()`: Add a new column based on an expression.
- `RENAME_COLUMN()`: Rename a column.
- `CAST()`: Change the data type of a column.
- `DROP_COLUMN()`: Remove one or more columns.
- `UNPIVOT()`: Transform columns into rows (melt).
- `GROUP_HAVING()`: Combine grouping and group filtering.

## Installation

You can install `seekwellpandas` via pip:

```bash
pip install seekwellpandas
```

## Usage

Here are some examples of how to use SeekwellPandas:

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
result = df.SELECT('A', 'B')

# Negative selection
result = df.SELECT('-A')

# Filter rows redirecting to .query() (the _ avoids overlapping with pandas.DataFrame.where)
result = df.WHERE('A > 2')

# Group and aggregate
result = df.GROUP_BY('B').AVG('A', "mean_A")

# Sort data
result = df.ORDER_BY('C', ascending=False)

# Add a new column
result = df.ADD_COLUMN('D', 'A * C')

# Join two DataFrames (the _ avoids overlapping with pandas.DataFrame.join)
df2 = pd.DataFrame({'B': ['a', 'b'], 'D': [100, 200]})
result = df.JOIN(df2, on='B')
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request on my GitHub repository.

## License

This project is licensed under the GPLv3 License. See the LICENSE file for details.
