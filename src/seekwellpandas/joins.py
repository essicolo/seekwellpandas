import pandas as pd
import pandas_flavor as pf
from .errors import InvalidJoinError, validate_columns_exist

@pf.register_dataframe_method
def JOIN(df, other, on=None, left_on=None, right_on=None, how='inner', suffixes=('_x', '_y')):
    """
    Join two DataFrames with enhanced syntax.

    Parameters:
    df (pd.DataFrame): The first DataFrame.
    other (pd.DataFrame): The second DataFrame.
    on (str or list, optional): The column(s) to join on (both DataFrames must have these columns).
    left_on (str or list, optional): Column(s) from the left DataFrame to join on.
    right_on (str or list, optional): Column(s) from the right DataFrame to join on.
    how (str): The type of join to perform ('inner', 'left', 'right', 'outer'). Default is 'inner'.
    suffixes (tuple): Suffixes for overlapping column names. Default is ('_x', '_y').

    Returns:
    pd.DataFrame: The joined DataFrame.
    """
    try:
        if on is not None:
            # Validate that join columns exist in both DataFrames
            validate_columns_exist(df, on, "LEFT JOIN")
            validate_columns_exist(other, on, "RIGHT JOIN")
            return df.merge(other, on=on, how=how, suffixes=suffixes)
        elif left_on is not None and right_on is not None:
            validate_columns_exist(df, left_on, "LEFT JOIN")
            validate_columns_exist(other, right_on, "RIGHT JOIN")
            return df.merge(other, left_on=left_on, right_on=right_on, how=how, suffixes=suffixes)
        else:
            raise InvalidJoinError(
                "Missing join condition",
                "Specify either 'on' parameter or both 'left_on' and 'right_on' parameters"
            )
    except Exception as e:
        if isinstance(e, (InvalidJoinError, ValueError)):
            raise
        else:
            raise InvalidJoinError(f"JOIN operation failed: {str(e)}")

@pf.register_dataframe_method
def LEFT_JOIN(df, other, on=None, left_on=None, right_on=None, suffixes=('_x', '_y')):
    """
    Perform a LEFT JOIN between two DataFrames.

    Parameters:
    df (pd.DataFrame): The left DataFrame.
    other (pd.DataFrame): The right DataFrame.
    on (str or list, optional): The column(s) to join on.
    left_on (str or list, optional): Column(s) from the left DataFrame to join on.
    right_on (str or list, optional): Column(s) from the right DataFrame to join on.
    suffixes (tuple): Suffixes for overlapping column names. Default is ('_x', '_y').

    Returns:
    pd.DataFrame: The joined DataFrame.
    """
    return JOIN(df, other, on=on, left_on=left_on, right_on=right_on, how='left', suffixes=suffixes)

@pf.register_dataframe_method
def RIGHT_JOIN(df, other, on=None, left_on=None, right_on=None, suffixes=('_x', '_y')):
    """
    Perform a RIGHT JOIN between two DataFrames.

    Parameters:
    df (pd.DataFrame): The left DataFrame.
    other (pd.DataFrame): The right DataFrame.
    on (str or list, optional): The column(s) to join on.
    left_on (str or list, optional): Column(s) from the left DataFrame to join on.
    right_on (str or list, optional): Column(s) from the right DataFrame to join on.
    suffixes (tuple): Suffixes for overlapping column names. Default is ('_x', '_y').

    Returns:
    pd.DataFrame: The joined DataFrame.
    """
    return JOIN(df, other, on=on, left_on=left_on, right_on=right_on, how='right', suffixes=suffixes)

@pf.register_dataframe_method
def FULL_JOIN(df, other, on=None, left_on=None, right_on=None, suffixes=('_x', '_y')):
    """
    Perform a FULL OUTER JOIN between two DataFrames.

    Parameters:
    df (pd.DataFrame): The left DataFrame.
    other (pd.DataFrame): The right DataFrame.
    on (str or list, optional): The column(s) to join on.
    left_on (str or list, optional): Column(s) from the left DataFrame to join on.
    right_on (str or list, optional): Column(s) from the right DataFrame to join on.
    suffixes (tuple): Suffixes for overlapping column names. Default is ('_x', '_y').

    Returns:
    pd.DataFrame: The joined DataFrame.
    """
    return JOIN(df, other, on=on, left_on=left_on, right_on=right_on, how='outer', suffixes=suffixes)
