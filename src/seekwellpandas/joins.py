import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def JOIN(df, other, on, how='inner'):
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
