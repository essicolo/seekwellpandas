# Seek well, pandas

`seekwellpandas` (SQL-pandas) is a pandas extension that provides SQL-inspired methods to manipulate DataFrames in a more intuitive way, closely resembling SQL syntax.

## Features

`seekwellpandas` adds the following methods to your pandas DataFrames:

- `select()`: Select specific columns, including negative selection.
- `where_()`: Filter rows based on a condition.
- `group_by()`: Group data by one or more columns.
- `having()`: Filter groups based on a condition.
- `order_by()`: Sort data by one or more columns.
- `limit()`: Limit the number of returned rows.
- `join_()`: Join two DataFrames.
- `union()`: Union two DataFrames.
- `distinct()`: Remove duplicates.
- `intersect()`: Find the intersection between two DataFrames.
- `difference()`: Find the difference between two DataFrames.
- `with_column()`: Add a new column based on an expression.
- `rename_column()`: Rename a column.
- `cast()`: Change the data type of a column.
- `drop_column()`: Remove one or more columns.
- `unpivot()`: Transform columns into rows (melt).
- `group_having()`: Combine grouping and group filtering.

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
result = df.select('A', 'B')

# Negative selection
result = df.select('-A')

# Filter rows redirecting to .query() (the _ avoids overlapping with pandas.DataFrame.where)
result = df.where_('A > 2')

# Group and aggregate
result = df.group_by('B').agg({'A': 'mean', 'C': 'sum'})

# Sort data
result = df.order_by('C', ascending=False)

# Add a new column
result = df.with_column('D', 'A * C')

# Join two DataFrames (the _ avoids overlapping with pandas.DataFrame.join)
df2 = pd.DataFrame({'B': ['a', 'b'], 'D': [100, 200]})
result = df.join_(df2, on='B')
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request on my GitHub repository.

## License

This project is licensed under the GPLv3 License. See the LICENSE file for details.
