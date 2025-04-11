import pandas as pd
import pandas_flavor as pf
from functools import wraps

# Create our own register_groupby_method decorator since pandas_flavor doesn't provide one
def register_groupby_method(method):
    """
    Register a function as a method of pd.core.groupby.GroupBy.
    
    Parameters
    ----------
    method : callable
        The method to be attached to pd.core.groupby.GroupBy.
    
    Returns
    -------
    callable
        The original method
    """
    @wraps(method)
    def wrapped(*args, **kwargs):
        return method(*args, **kwargs)
    
    setattr(pd.core.groupby.GroupBy, method.__name__, wrapped)
    return method

@pf.register_dataframe_method
@register_groupby_method  # This allows the method to be used on GroupBy objects
def COUNT(df, target_column=None, result_name=None):
    """
    Perform a SQL-like COUNT aggregation.

    Parameters:
    df (pd.DataFrame or pd.core.groupby.DataFrameGroupBy): The DataFrame or grouped DataFrame to aggregate.
    target_column (str): The column to count. If None and df is a GroupBy object, counts all rows.
    result_name (str, optional): Name for the result column. Defaults to '{target_column}_count'.

    Returns:
    pd.DataFrame: A DataFrame with the count results.
    """
    if isinstance(df, pd.core.groupby.GroupBy):
        if target_column is None:
            # Count all rows in each group if no column specified
            result = df.size().reset_index()
            col_name = result_name or 'count'
            result.columns = list(result.columns[:-1]) + [col_name]
            return result
        else:
            col_name = result_name or f'{target_column}_count'
            return df[target_column].count().reset_index(name=col_name)
    else:
        raise ValueError("This method must be used after GROUP_BY.")

@pf.register_dataframe_method
@register_groupby_method
def SUM(df, target_column, result_name=None):
    """
    Perform a SQL-like SUM aggregation.

    Parameters:
    df (pd.DataFrame or pd.core.groupby.DataFrameGroupBy): The DataFrame or grouped DataFrame to aggregate.
    target_column (str): The column to sum.
    result_name (str, optional): Name for the result column. Defaults to '{target_column}_sum'.

    Returns:
    pd.DataFrame: A DataFrame with the sum results.
    """
    if isinstance(df, pd.core.groupby.GroupBy):
        col_name = result_name or f'{target_column}_sum'
        return df[target_column].sum().reset_index(name=col_name)
    else:
        raise ValueError("This method must be used after GROUP_BY.")

@pf.register_dataframe_method
@register_groupby_method
def AVG(df, target_column, result_name=None):
    """
    Perform a SQL-like AVG aggregation.

    Parameters:
    df (pd.DataFrame or pd.core.groupby.DataFrameGroupBy): The DataFrame or grouped DataFrame to aggregate.
    target_column (str): The column to average.
    result_name (str, optional): Name for the result column. Defaults to '{target_column}_avg'.

    Returns:
    pd.DataFrame: A DataFrame with the average results.
    """
    if isinstance(df, pd.core.groupby.GroupBy):
        col_name = result_name or f'{target_column}_avg'
        return df[target_column].mean().reset_index(name=col_name)
    else:
        raise ValueError("This method must be used after GROUP_BY.")

@pf.register_dataframe_method
@register_groupby_method
def MIN(df, target_column, result_name=None):
    """
    Perform a SQL-like MIN aggregation.

    Parameters:
    df (pd.DataFrame or pd.core.groupby.DataFrameGroupBy): The DataFrame or grouped DataFrame to aggregate.
    target_column (str): The column to find the minimum value.
    result_name (str, optional): Name for the result column. Defaults to '{target_column}_min'.

    Returns:
    pd.DataFrame: A DataFrame with the minimum results.
    """
    if isinstance(df, pd.core.groupby.GroupBy):
        col_name = result_name or f'{target_column}_min'
        return df[target_column].min().reset_index(name=col_name)
    else:
        raise ValueError("This method must be used after GROUP_BY.")

@pf.register_dataframe_method
@register_groupby_method
def MAX(df, target_column, result_name=None):
    """
    Perform a SQL-like MAX aggregation.

    Parameters:
    df (pd.DataFrame or pd.core.groupby.DataFrameGroupBy): The DataFrame or grouped DataFrame to aggregate.
    target_column (str): The column to find the maximum value.
    result_name (str, optional): Name for the result column. Defaults to '{target_column}_max'.

    Returns:
    pd.DataFrame: A DataFrame with the maximum results.
    """
    if isinstance(df, pd.core.groupby.GroupBy):
        col_name = result_name or f'{target_column}_max'
        return df[target_column].max().reset_index(name=col_name)
    else:
        raise ValueError("This method must be used after GROUP_BY.")
