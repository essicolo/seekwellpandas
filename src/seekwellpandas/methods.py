import warnings
import pandas as pd

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