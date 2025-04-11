"""
Aliases for seekwellpandas methods.

This module provides lowercase aliases for all seekwellpandas methods.
Where there is overlap with pandas methods, an underscore is appended to the name.
"""

import pandas as pd
import pandas_flavor as pf
from functools import wraps

# Aggregate methods
@pf.register_dataframe_method
def count_(df, target_column=None, result_name=None):
    """Lowercase alias for COUNT method."""
    from .aggregate import COUNT
    return COUNT(df, target_column, result_name)

@pf.register_dataframe_method
def sum_(df, target_column, result_name=None):
    """Lowercase alias for SUM method."""
    from .aggregate import SUM
    return SUM(df, target_column, result_name)

@pf.register_dataframe_method
def avg(df, target_column, result_name=None):
    """Lowercase alias for AVG method."""
    from .aggregate import AVG
    return AVG(df, target_column, result_name)

@pf.register_dataframe_method
def min_(df, target_column, result_name=None):
    """Lowercase alias for MIN method."""
    from .aggregate import MIN
    return MIN(df, target_column, result_name)

@pf.register_dataframe_method
def max_(df, target_column, result_name=None):
    """Lowercase alias for MAX method."""
    from .aggregate import MAX
    return MAX(df, target_column, result_name)

# Miscellaneous methods
@pf.register_dataframe_method
def truncate(df):
    """Lowercase alias for TRUNCATE method."""
    from .miscellaneous import TRUNCATE
    return TRUNCATE(df)

@pf.register_dataframe_method
def alter_table(df, add_columns=None, drop_columns=None):
    """Lowercase alias for ALTER_TABLE method."""
    from .miscellaneous import ALTER_TABLE
    return ALTER_TABLE(df, add_columns, drop_columns)

@pf.register_dataframe_method
def merge_(df, other, on, how='inner'):
    """Lowercase alias for MERGE method."""
    from .miscellaneous import MERGE
    return MERGE(df, other, on, how)

@pf.register_dataframe_method
def limit(df, n):
    """Lowercase alias for LIMIT method."""
    from .miscellaneous import LIMIT
    return LIMIT(df, n)

@pf.register_dataframe_method
def distinct(df):
    """Lowercase alias for DISTINCT method."""
    from .miscellaneous import DISTINCT
    return DISTINCT(df)

@pf.register_dataframe_method
def union(df, other):
    """Lowercase alias for UNION method."""
    from .miscellaneous import UNION
    return UNION(df, other)

@pf.register_dataframe_method
def intersect(df, other):
    """Lowercase alias for INTERSECT method."""
    from .miscellaneous import INTERSECT
    return INTERSECT(df, other)

@pf.register_dataframe_method
def difference(df, other):
    """Lowercase alias for DIFFERENCE method."""
    from .miscellaneous import DIFFERENCE
    return DIFFERENCE(df, other)

@pf.register_dataframe_method
def add_column(df, column_name, expression):
    """Lowercase alias for ADD_COLUMN method."""
    from .miscellaneous import ADD_COLUMN
    return ADD_COLUMN(df, column_name, expression)

@pf.register_dataframe_method
def rename_column(df, old_name, new_name):
    """Lowercase alias for RENAME_COLUMN method."""
    from .miscellaneous import RENAME_COLUMN
    return RENAME_COLUMN(df, old_name, new_name)

@pf.register_dataframe_method
def delete(df, condition):
    """Lowercase alias for DELETE method."""
    from .miscellaneous import DELETE
    return DELETE(df, condition)

@pf.register_dataframe_method
def update(df, condition, updates):
    """Lowercase alias for UPDATE method."""
    from .miscellaneous import UPDATE
    return UPDATE(df, condition, updates)

@pf.register_dataframe_method
def insert(df, new_rows):
    """Lowercase alias for INSERT method."""
    from .miscellaneous import INSERT
    return INSERT(df, new_rows)

# Methods from other modules
@pf.register_dataframe_method
def select(df, *columns):
    """Lowercase alias for SELECT method."""
    from .methods import SELECT
    return SELECT(df, *columns)

@pf.register_dataframe_method
def where(df, condition):
    """Lowercase alias for WHERE method."""
    from .methods import WHERE
    return WHERE(df, condition)

@pf.register_dataframe_method
def group_by(df, *columns):
    """Lowercase alias for GROUP_BY method."""
    from .methods import GROUP_BY
    return GROUP_BY(df, *columns)

@pf.register_dataframe_method
def order_by(df, columns, ascending=True):
    """Lowercase alias for ORDER_BY method."""
    from .methods import ORDER_BY
    return ORDER_BY(df, columns, ascending)

@pf.register_dataframe_method
def join_(df, other, on, how='inner'):
    """Lowercase alias for JOIN method."""
    from .methods import JOIN
    return JOIN(df, other, on, how)

# Register GroupBy methods
def _register_groupby_aliases():
    """Register lowercase aliases for GroupBy methods."""
    # Need to first import the aggregate module to ensure GroupBy methods are registered
    from . import aggregate
    
    # Create a mapping of uppercase method names to their lowercase aliases
    method_map = {
        'COUNT': 'count_',
        'SUM': 'sum_',
        'AVG': 'avg',
        'MIN': 'min_',
        'MAX': 'max_'
    }
    
    # Register each lowercase alias as a GroupBy method
    for upper_name, lower_name in method_map.items():
        if hasattr(pd.core.groupby.GroupBy, upper_name):
            original_method = getattr(pd.core.groupby.GroupBy, upper_name)
            
            @wraps(original_method)
            def create_wrapped(upper_method=original_method):
                def wrapped_method(*args, **kwargs):
                    return upper_method(*args, **kwargs)
                return wrapped_method
            
            setattr(pd.core.groupby.GroupBy, lower_name, create_wrapped())

# Call this function to register the GroupBy aliases
_register_groupby_aliases()
