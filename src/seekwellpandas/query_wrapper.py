import pandas as pd

class QueryWrapper:
    def __init__(self, dataframe, aggregation=None, alias=None):
        self.dataframe = dataframe
        self.aggregation = aggregation
        self.alias = alias

    def __getattr__(self, name):
        """
        Automatically wrap the DataFrame when a seekwellpandas method is called.

        Parameters:
        name (str): The name of the method being accessed.

        Returns:
        callable: A wrapped method if it exists in seekwellpandas, otherwise raises AttributeError.
        """
        if hasattr(self.dataframe, name):
            attr = getattr(self.dataframe, name)
            if callable(attr):
                def wrapped_method(*args, **kwargs):
                    result = attr(*args, **kwargs)
                    if isinstance(result, pd.DataFrame):
                        return QueryWrapper(result)
                    return result
                return wrapped_method
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def SELECT(self, *args, columns=None, aggregate=None, alias=None):
        """
        Select specific columns from the DataFrame, including negative selection and aggregation.

        Parameters:
        *args: Columns to select (for backward compatibility).
        columns (list or None): The columns to select. Can be strings or lists.
                                Prefix column names with '-' for negative selection.
        aggregate (dict or None): A dictionary specifying columns to aggregate and their functions.
        alias (str or None): Alias for the aggregated column.

        Returns:
        QueryWrapper: A new QueryWrapper instance with updated metadata.
        """
        if columns is None:
            columns = args

        if aggregate:
            # Return a new QueryWrapper instance with aggregation and alias metadata
            return QueryWrapper(self.dataframe, aggregation=aggregate, alias=alias)

        all_columns = set(self.dataframe.columns)
        selected_columns = set()
        excluded_columns = set()

        for col in columns:
            if isinstance(col, list):
                for item in col:
                    self._process_column(item, all_columns, selected_columns, excluded_columns)
            elif isinstance(col, str):
                self._process_column(col, all_columns, selected_columns, excluded_columns)

        if selected_columns:
            final_columns = selected_columns - excluded_columns
        else:
            final_columns = all_columns - excluded_columns

        # Return a new QueryWrapper instance with the selected columns
        return QueryWrapper(self.dataframe[list(final_columns)])

    def GROUP_BY(self, *columns):
        """
        Group the DataFrame by specific columns and apply aggregation if available.

        Parameters:
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

        grouped = self.dataframe.groupby(group_columns)

        if self.aggregation:
            result = grouped.agg(self.aggregation)

            if self.alias:
                result = result.rename(columns={list(self.aggregation.keys())[0]: self.alias})

            return result

        return grouped

    def _process_column(self, col, all_columns, selected_columns, excluded_columns):
        """
        Internal method to process a single column for selection.
        """
        if col.startswith('-'):
            col_name = col[1:]
            excluded_columns.add(col_name)
        else:
            selected_columns.add(col)

# Add a `query` property to pandas DataFrame
@property
def query(df):
    """
    Attach a `query` property to pandas DataFrame to return a QueryWrapper instance.

    Returns:
    QueryWrapper: A QueryWrapper instance for the DataFrame.
    """
    return QueryWrapper(df)

# Register the `query` property to pandas DataFrame
pd.DataFrame.query = query
