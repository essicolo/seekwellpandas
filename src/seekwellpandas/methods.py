import pandas as pd
import pandas_flavor as pf
import warnings

@pf.register_dataframe_method
def select(df, *columns):
    """
    Select specific columns from the DataFrame, including negative selection.

    Parameters:
    df (pd.DataFrame): The DataFrame to select columns from.
    *columns (str or list): The columns to select. Can be strings or lists.
                            Prefix column names with '-' for negative selection.

    Returns:
    pd.DataFrame: A DataFrame with the selected columns.
    """
    all_columns = set(df.columns)
    selected_columns = set()
    excluded_columns = set()

    for col in columns:
        if isinstance(col, list):
            for item in col:
                _process_column(item, all_columns, selected_columns, excluded_columns)
        elif isinstance(col, str):
            _process_column(col, all_columns, selected_columns, excluded_columns)

    if selected_columns:
        final_columns = selected_columns - excluded_columns
    else:
        final_columns = all_columns - excluded_columns

    return df[list(final_columns)]

def _process_column(col, all_columns, selected_columns, excluded_columns):
    """
    Internal method to process a single column for selection.

    Parameters:
    col (str): The column to process.
    all_columns (set): A set of all columns in the DataFrame.
    selected_columns (set): A set of columns to select.
    excluded_columns (set): A set of columns to exclude.

    Returns:
    None

    """
    if col.startswith('-'):
        col_name = col[1:]
        excluded_columns.add(col_name)
        if col in all_columns:
            warnings.warn(f"Column '{col}' Already exists in the data frame. "
                          f"Make sure that you meant to exclude '{col_name}', and not select '{col}'.")
    else:
        selected_columns.add(col)

@pf.register_dataframe_method
def where_(df, condition):
    """
    Filter the DataFrame based on a condition.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    condition (str or list): The condition(s) to filter by. Can be a string or a list of strings.

    Returns:
    pd.DataFrame: A filtered DataFrame.
    """
    if isinstance(condition, list):
        condition = ' and '.join(f'({cond})' for cond in condition)
    return df.query(condition)

@pf.register_dataframe_method
def group_by(df, *columns):
    """
    Group the DataFrame by specific columns.

    Parameters:
    df (pd.DataFrame): The DataFrame to group.
    *columns (str or list): The columns to group by. Can be strings or lists.

    Returns:
    pd.core.groupby.DataFrameGroupBy: A grouped DataFrame.
    """
    group_columns = []
    for col in columns:
        if isinstance(col, list):
            group_columns.extend(col)
        else:
            group_columns.append(col)
    return df.groupby(group_columns)

@pf.register_dataframe_method
def having(df, condition):
    """
    Filter groups in the DataFrame based on a condition.

    Parameters:
    df (pd.core.groupby.GroupBy): The grouped DataFrame to filter.
    condition (str): The condition to filter by.

    Returns:
    pd.DataFrame: A DataFrame with the filtered groups.

    Raises:
    ValueError: If the DataFrame is not grouped.
    """
    if isinstance(df, pd.core.groupby.GroupBy):
        return df.filter(condition)
    else:
        raise ValueError("having can only be used after group_by")

@pf.register_dataframe_method
def order_by(df, column, ascending=True):
    """
    Sort the DataFrame by specific columns.

    Parameters:
    df (pd.DataFrame): The DataFrame to sort.
    *columns (str or list): The columns to sort by. Can be strings or lists.
    ascending (bool or list): Whether to sort in ascending order. Can be a single boolean or a list.

    Returns:
    pd.DataFrame: A sorted DataFrame.
    """
    sort_columns = []
    for col in columns:
        if isinstance(col, list):
            sort_columns.extend(col)
        else:
            sort_columns.append(col)
    
    if isinstance(ascending, bool):
        ascending = [ascending] * len(sort_columns)
    
    return df.sort_values(sort_columns, ascending=ascending)

@pf.register_dataframe_method
def limit(df, n):
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
def join_(df, other, on, how='inner'):
    """
    Join two DataFrames.

    Parameters:
    df (pd.DataFrame): The first DataFrame.
    other (pd.DataFrame): The second DataFrame.
    on (str or list): The column(s) to join on.
    how (str): The type of join to perform. Default is 'inner'.

    Returns:
    pd.DataFrame: The joined DataFrame.
    """
    return df.merge(other, on=on, how=how)

@pf.register_dataframe_method
def union(df, other):
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
def distinct(df):
    """
    Remove duplicate rows from the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to remove duplicates from.

    Returns:
    pd.DataFrame: A DataFrame with duplicate rows removed.
    """
    return df.drop_duplicates()

@pf.register_dataframe_method
def intersect(df, other):
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
def difference(df, other):
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
def with_column(df, name, expression):
    """
    Add a new column to the DataFrame based on an expression.

    Parameters:
    df (pd.DataFrame): The DataFrame to add the column to.
    name (str): The name of the new column.
    expression (str): The expression to calculate the new column.

    Returns:
    pd.DataFrame: The DataFrame with the new column added.
    """
    df[name] = df.eval(expression)
    return df

@pf.register_dataframe_method
def rename_column(df, old_name, new_name):
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
def cast(df, column, dtype):
    """
    Cast a column to a different data type.

    Parameters:
    df (pd.DataFrame): The DataFrame to cast the column in.
    column (str): The column to cast.
    dtype (str or type): The data type to cast to.

    Returns:
    pd.DataFrame: The DataFrame with the casted column.
    """
    df[column] = df[column].astype(dtype)
    return df

@pf.register_dataframe_method
def drop_column(df, *columns):
    """
    Drop specific columns from the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to drop columns from.
    *columns (str): The columns to drop.

    Returns:
    pd.DataFrame: A DataFrame with the specified columns dropped.
    """
    return df.drop(columns=list(columns))

@pf.register_dataframe_method
def unpivot(df, id_vars, value_vars, var_name, value_name):
    """
    Unpivot the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to unpivot.
    id_vars (str or list): The column(s) to use as identifier variables.
    value_vars (str or list): The column(s) to unpivot.
    var_name (str): The name of the variable column.
    value_name (str): The name of the value column.

    Returns:
    pd.DataFrame: An unpivoted DataFrame.
    """
    return df.melt(id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

# Méthode spécifique pour les groupby
@pf.register_dataframe_method
def group_having(df, groupby_columns, having_condition):
    return df.groupby(groupby_columns).filter(having_condition)

__all__ = ['select', 'where_', 'group_by', 'having', 'order_by', 'limit', 'join_', 'union', 'distinct', 
           'intersect', 'difference', 'create_view', 'with_column', 'rename_column', 'cast', 'drop_column', 
            'unpivot', 'group_having']