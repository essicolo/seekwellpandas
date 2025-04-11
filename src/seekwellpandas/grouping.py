from .query_wrapper import QueryWrapper
import pandas_flavor as pf

@pf.register_dataframe_method
def GROUP_BY(df, *columns):
    """
    Group the DataFrame by specific columns and apply aggregation if available.

    Parameters:
    df (pd.DataFrame): The DataFrame to group.
    *columns (str or list): The columns to group by.

    Returns:
    pd.DataFrame: A grouped and aggregated DataFrame if aggregation is defined.
    """
    group_columns = []
    for col in columns:
        if isinstance(col, list):
            group_columns.extend(col)
        else:
            group_columns.append(col)

    grouped = df.groupby(group_columns)

    if isinstance(df, QueryWrapper) and df.aggregation:
        result = grouped.agg(df.aggregation)

        if df.alias:
            result = result.rename(columns={list(df.aggregation.keys())[0]: df.alias})

        return result

    return grouped
