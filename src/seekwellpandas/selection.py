from .methods import _process_column
from .query_wrapper import QueryWrapper

import pandas_flavor as pf

@pf.register_dataframe_method
def SELECT(df, *args, columns=None, aggregate=None, alias=None):
    """
    Select specific columns from the DataFrame, including negative selection and aggregation.

    Parameters:
    df (pd.DataFrame): The DataFrame to select columns from.
    *args: Columns to select (for backward compatibility).
    columns (list or None): The columns to select. Can be strings or lists.
                            Prefix column names with '-' for negative selection.
    aggregate (dict or None): A dictionary specifying columns to aggregate and their functions.
    alias (str or None): Alias for the aggregated column.

    Returns:
    QueryWrapper: A QueryWrapper instance for chaining.
    """
    if columns is None:
        columns = args

    if aggregate:
        return QueryWrapper(df, aggregation=aggregate, alias=alias)

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

    return QueryWrapper(df[list(final_columns)])
