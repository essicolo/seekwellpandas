import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def TRUNCATE(df):
    """
    Remove all rows from the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to truncate.

    Returns:
    pd.DataFrame: An empty DataFrame with the same columns.
    """
    return df.iloc[0:0]

@pf.register_dataframe_method
def ALTER_TABLE(df, add_columns=None, drop_columns=None):
    """
    Modify the structure of the DataFrame by adding or dropping columns.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    add_columns (dict): A dictionary where keys are column names and values are default values for new columns.
    drop_columns (list): A list of column names to drop.

    Returns:
    pd.DataFrame: The modified DataFrame.
    """
    if add_columns:
        for col, default in add_columns.items():
            df[col] = default
    if drop_columns:
        df = df.drop(columns=drop_columns)
    return df

@pf.register_dataframe_method
def MERGE(df, other, on, how='inner'):
    """
    Merge two DataFrames based on a condition.

    Parameters:
    df (pd.DataFrame): The first DataFrame.
    other (pd.DataFrame): The second DataFrame.
    on (str or list): Column(s) to join on.
    how (str): Type of merge to perform ('inner', 'outer', 'left', 'right').

    Returns:
    pd.DataFrame: The merged DataFrame.
    """
    return pd.merge(df, other, on=on, how=how)

@pf.register_dataframe_method
def LIMIT(df, n):
    """
    Limit the number of rows in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to limit.
    n (int): The number of rows to return.

    Returns:
    pd.DataFrame: A DataFrame with the limited number of rows.
    """
    return df.head(n)

@pf.register_dataframe_method
def DISTINCT(df):
    """
    Remove duplicate rows from the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to remove duplicates from.

    Returns:
    pd.DataFrame: A DataFrame with duplicate rows removed.
    """
    return df.drop_duplicates()

@pf.register_dataframe_method
def UNION(df, other):
    """
    Union two DataFrames.

    Parameters:
    df (pd.DataFrame): The first DataFrame.
    other (pd.DataFrame): The second DataFrame.

    Returns:
    pd.DataFrame: The union of the two DataFrames.
    """
    return pd.concat([df, other], axis=0, ignore_index=True)

@pf.register_dataframe_method
def INTERSECT(df, other):
    """
    Intersect two DataFrames.

    Parameters:
    df (pd.DataFrame): The first DataFrame.
    other (pd.DataFrame): The second DataFrame.

    Returns:
    pd.DataFrame: The intersection of the two DataFrames.
    """
    return pd.merge(df, other, how='inner')

@pf.register_dataframe_method
def DIFFERENCE(df, other):
    """
    Find the difference between two DataFrames.

    Parameters:
    df (pd.DataFrame): The first DataFrame.
    other (pd.DataFrame): The second DataFrame.

    Returns:
    pd.DataFrame: The difference between the two DataFrames.
    """
    return df[~df.apply(tuple, 1).isin(other.apply(tuple, 1))]

@pf.register_dataframe_method
def ADD_COLUMN(df, column_name, expression):
    """
    Add a new column to the DataFrame based on an expression.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    column_name (str): The name of the new column.
    expression (str): A string representing the expression to compute the new column.

    Returns:
    pd.DataFrame: The DataFrame with the new column added.
    """
    df[column_name] = df.eval(expression)
    return df

@pf.register_dataframe_method
def RENAME_COLUMN(df, old_name, new_name):
    """
    Rename a column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to rename the column in.
    old_name (str): The old name of the column.
    new_name (str): The new name of the column.

    Returns:
    pd.DataFrame: The DataFrame with the renamed column.
    """
    return df.rename(columns={old_name: new_name})


@pf.register_dataframe_method
def DELETE(df, condition):
    """
    Remove rows from the DataFrame based on a condition.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    condition (str): A string representing the condition in SQL-like syntax.

    Returns:
    pd.DataFrame: A DataFrame with rows removed based on the condition.

    Examples:
    df.delete('A > 5')
    """
    return df[~df.eval(condition)]


@pf.register_dataframe_method
def UPDATE(df, condition, updates):
    """
    Update values in the DataFrame based on a condition.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    condition (str): A string representing the condition in SQL-like syntax.
    updates (dict): A dictionary where keys are column names and values are the new values or expressions.

    Returns:
    pd.DataFrame: A DataFrame with updated values.

    Examples:
    df.UPDATE('age > 30', {'city': 'Updated City'})
    """
    mask = df.eval(condition)
    for column, value in updates.items():
        if isinstance(value, str):
            df.loc[mask, column] = value  # Directly assign string values
        else:
            df.loc[mask, column] = df.loc[mask].eval(value) if isinstance(value, str) else value
    return df


@pf.register_dataframe_method
def INSERT(df, new_rows):
    """
    Insert new rows into the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    new_rows (pd.DataFrame): A DataFrame containing the new rows to insert.

    Returns:
    pd.DataFrame: A DataFrame with the new rows appended.

    Examples:
    new_data = pd.DataFrame({'A': [5, 6], 'B': ['x', 'y']})
    df.insert(new_data)
    """
    return pd.concat([df, new_rows], ignore_index=True)

@pf.register_dataframe_method
def PIVOT(df, index=None, columns=None, values=None, aggfunc='mean', fill_value=None):
    """
    Pivot the DataFrame from long to wide format, similar to SQL PIVOT.

    Parameters:
    df (pd.DataFrame): The DataFrame to pivot.
    index (str or list, optional): Column(s) to use as row identifiers.
    columns (str or list): Column(s) to use as new column headers.
    values (str or list, optional): Column(s) to aggregate.
    aggfunc (str or function): Aggregation function to use. Default is 'mean'.
    fill_value: Value to use for missing data. Default is None.

    Returns:
    pd.DataFrame: The pivoted DataFrame.

    Examples:
    df.PIVOT(index='date', columns='product', values='sales')
    """
    if values is None:
        # If no values specified, use all numeric columns
        numeric_cols = df.select_dtypes(include=[pd.api.types.is_numeric_dtype]).columns
        if index is not None:
            if isinstance(index, str):
                index = [index]
            numeric_cols = numeric_cols.difference(index)
        if columns is not None:
            if isinstance(columns, str):
                columns = [columns]
            numeric_cols = numeric_cols.difference(columns)
        values = numeric_cols.tolist()

    return df.pivot_table(
        index=index,
        columns=columns,
        values=values,
        aggfunc=aggfunc,
        fill_value=fill_value
    )
