import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def ROW_NUMBER(df, partition_by=None, order_by=None, ascending=True):
    """
    Add row numbers to the DataFrame, similar to SQL ROW_NUMBER() OVER().

    Parameters:
    df (pd.DataFrame): The DataFrame to add row numbers to.
    partition_by (str or list, optional): Column(s) to partition by.
    order_by (str or list, optional): Column(s) to order by.
    ascending (bool or list, optional): Sort order. Default is True.

    Returns:
    pd.DataFrame: DataFrame with row_number column added.
    """
    result_df = df.copy()

    if partition_by is None:
        # No partitioning, just add row numbers
        if order_by is not None:
            result_df = result_df.sort_values(order_by, ascending=ascending)
        result_df['row_number'] = range(1, len(result_df) + 1)
    else:
        # Partition by specified columns
        if isinstance(partition_by, str):
            partition_by = [partition_by]

        def add_row_number(group):
            if order_by is not None:
                group = group.sort_values(order_by, ascending=ascending)
            group['row_number'] = range(1, len(group) + 1)
            return group

        result_df = result_df.groupby(partition_by, group_keys=False).apply(add_row_number)

    return result_df

@pf.register_dataframe_method
def RANK(df, order_by, partition_by=None, ascending=False, method='min'):
    """
    Add rankings to the DataFrame, similar to SQL RANK() OVER().

    Parameters:
    df (pd.DataFrame): The DataFrame to add rankings to.
    order_by (str or list): Column(s) to order by for ranking.
    partition_by (str or list, optional): Column(s) to partition by.
    ascending (bool or list, optional): Sort order. Default is False (highest first).
    method (str): Ranking method ('min', 'max', 'average', 'first', 'dense').

    Returns:
    pd.DataFrame: DataFrame with rank column added.
    """
    result_df = df.copy()

    if partition_by is None:
        # No partitioning, rank entire DataFrame
        result_df['rank'] = result_df[order_by].rank(method=method, ascending=ascending)
    else:
        # Partition by specified columns
        if isinstance(partition_by, str):
            partition_by = [partition_by]

        def add_rank(group):
            group['rank'] = group[order_by].rank(method=method, ascending=ascending)
            return group

        result_df = result_df.groupby(partition_by, group_keys=False).apply(add_rank)

    return result_df

@pf.register_dataframe_method
def DENSE_RANK(df, order_by, partition_by=None, ascending=False):
    """
    Add dense rankings to the DataFrame, similar to SQL DENSE_RANK() OVER().

    Parameters:
    df (pd.DataFrame): The DataFrame to add dense rankings to.
    order_by (str or list): Column(s) to order by for ranking.
    partition_by (str or list, optional): Column(s) to partition by.
    ascending (bool or list, optional): Sort order. Default is False (highest first).

    Returns:
    pd.DataFrame: DataFrame with dense_rank column added.
    """
    return RANK(df, order_by=order_by, partition_by=partition_by,
                ascending=ascending, method='dense').rename(columns={'rank': 'dense_rank'})

@pf.register_dataframe_method
def LAG(df, column, partition_by=None, order_by=None, periods=1, fill_value=None):
    """
    Get the previous value in a column, similar to SQL LAG().

    Parameters:
    df (pd.DataFrame): The DataFrame to process.
    column (str): The column to get previous values from.
    partition_by (str or list, optional): Column(s) to partition by.
    order_by (str or list, optional): Column(s) to order by.
    periods (int): Number of periods to shift. Default is 1.
    fill_value: Value to use for missing values.

    Returns:
    pd.DataFrame: DataFrame with lag column added.
    """
    result_df = df.copy()

    if partition_by is None:
        # No partitioning
        if order_by is not None:
            result_df = result_df.sort_values(order_by)
        result_df[f'{column}_lag'] = result_df[column].shift(periods, fill_value=fill_value)
    else:
        # Partition by specified columns
        if isinstance(partition_by, str):
            partition_by = [partition_by]

        def add_lag(group):
            if order_by is not None:
                group = group.sort_values(order_by)
            group[f'{column}_lag'] = group[column].shift(periods, fill_value=fill_value)
            return group

        result_df = result_df.groupby(partition_by, group_keys=False).apply(add_lag)

    return result_df

@pf.register_dataframe_method
def LEAD(df, column, partition_by=None, order_by=None, periods=1, fill_value=None):
    """
    Get the next value in a column, similar to SQL LEAD().

    Parameters:
    df (pd.DataFrame): The DataFrame to process.
    column (str): The column to get next values from.
    partition_by (str or list, optional): Column(s) to partition by.
    order_by (str or list, optional): Column(s) to order by.
    periods (int): Number of periods to shift. Default is 1.
    fill_value: Value to use for missing values.

    Returns:
    pd.DataFrame: DataFrame with lead column added.
    """
    result_df = df.copy()

    if partition_by is None:
        # No partitioning
        if order_by is not None:
            result_df = result_df.sort_values(order_by)
        result_df[f'{column}_lead'] = result_df[column].shift(-periods, fill_value=fill_value)
    else:
        # Partition by specified columns
        if isinstance(partition_by, str):
            partition_by = [partition_by]

        def add_lead(group):
            if order_by is not None:
                group = group.sort_values(order_by)
            group[f'{column}_lead'] = group[column].shift(-periods, fill_value=fill_value)
            return group

        result_df = result_df.groupby(partition_by, group_keys=False).apply(add_lead)

    return result_df
