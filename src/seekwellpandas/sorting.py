import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def ORDER_BY(df, columns, ascending=True):
    """
    Sort the DataFrame by specific columns.

    Parameters:
    df (pd.DataFrame): The DataFrame to sort.
    columns (str or list): The columns to sort by. Can be strings or lists.
    ascending (bool or list): Whether to sort in ascending order. Can be a single boolean or a list.

    Returns:
    pd.DataFrame: A sorted DataFrame.
    """
    if not isinstance(columns, list):
        columns = [columns]
    sort_columns = []
    for col in columns:
        if isinstance(col, list):
            sort_columns.extend(col)
        else:
            sort_columns.append(col)

    if isinstance(ascending, bool):
        ascending = [ascending] * len(sort_columns)

    return df.sort_values(sort_columns, ascending=ascending)
