import pandas as pd
import pandas_flavor as pf
import numpy as np

class CaseBuilder:
    """
    A builder class for creating SQL-like CASE statements.
    """

    def __init__(self, df):
        self.df = df
        self.conditions = []
        self.values = []
        self.else_value = None

    def WHEN(self, condition, value):
        """
        Add a WHEN condition to the CASE statement.

        Parameters:
        condition (str or pd.Series): The condition to evaluate.
        value: The value to return when the condition is True.

        Returns:
        CaseBuilder: The current CaseBuilder instance for chaining.
        """
        if isinstance(condition, str):
            # Parse the condition string similar to WHERE
            parsed_condition = self._parse_condition(condition)
            self.conditions.append(parsed_condition)
        else:
            # Assume it's already a boolean Series
            self.conditions.append(condition)

        self.values.append(value)
        return self

    def ELSE(self, value):
        """
        Set the ELSE value for the CASE statement.

        Parameters:
        value: The value to return when no conditions are met.

        Returns:
        CaseBuilder: The current CaseBuilder instance for chaining.
        """
        self.else_value = value
        return self

    def END(self, column_name):
        """
        Complete the CASE statement and add the result as a new column.

        Parameters:
        column_name (str): The name of the new column.

        Returns:
        pd.DataFrame: The DataFrame with the new conditional column.
        """
        result_df = self.df.copy()

        # Create the result series with else_value as default
        if self.else_value is not None:
            result_series = pd.Series([self.else_value] * len(self.df), index=self.df.index)
        else:
            result_series = pd.Series([np.nan] * len(self.df), index=self.df.index)

        # Apply conditions in reverse order (last condition has highest priority)
        for condition, value in zip(reversed(self.conditions), reversed(self.values)):
            result_series = result_series.where(~condition, value)

        result_df[column_name] = result_series
        return result_df

    def _parse_condition(self, condition):
        """
        Parse a condition string into a boolean Series.
        Similar to WHERE condition parsing.
        """
        import re

        def parse_value(column, value):
            value = value.strip()
            column_dtype = self.df[column].dtype
            if pd.api.types.is_numeric_dtype(column_dtype):
                try:
                    return float(value)
                except ValueError:
                    return pd.NA
            elif pd.api.types.is_datetime64_any_dtype(column_dtype):
                try:
                    return pd.to_datetime(value)
                except ValueError:
                    return pd.NaT
            else:
                return value.strip("'\"")

        def parse_in_condition(column, values):
            parsed_values = [parse_value(column, v.strip()) for v in values.split(',')]
            return self.df[column].isin(parsed_values)

        def parse_single_condition(cond):
            in_match = re.match(r'(\w+)\s+(not\s+in|in)\s+(.*)', cond)
            if in_match:
                column, op, values = in_match.groups()
                result = parse_in_condition(column, values)
                return ~result if op == "not in" else result

            ops = {
                '==': lambda x, y: x == y,
                '!=': lambda x, y: x != y,
                '>=': lambda x, y: x >= y,
                '<=': lambda x, y: x <= y,
                '>': lambda x, y: x > y,
                '<': lambda x, y: x < y
            }
            for op in sorted(ops.keys(), key=len, reverse=True):
                if op in cond:
                    column, value = cond.split(op)
                    column = column.strip()
                    value = value.strip()
                    parsed_value = parse_value(column, value)
                    if pd.isna(parsed_value):
                        return pd.Series(False, index=self.df.index)
                    return ops[op](self.df[column], parsed_value)

            return pd.Series(True, index=self.df.index)

        condition_parts = re.split(r'\s+and\s+|\s+or\s+', condition)
        parsed_conditions = [parse_single_condition(part) for part in condition_parts]

        final_condition = parsed_conditions[0]
        for i, part in enumerate(re.findall(r'\s+(and|or)\s+', condition)):
            if part == 'and':
                final_condition = final_condition & parsed_conditions[i+1]
            else:  # 'or'
                final_condition = final_condition | parsed_conditions[i+1]

        return final_condition


@pf.register_dataframe_method
def CASE(df):
    """
    Start a SQL-like CASE statement.

    Parameters:
    df (pd.DataFrame): The DataFrame to apply the CASE statement to.

    Returns:
    CaseBuilder: A CaseBuilder instance for constructing the CASE statement.

    Example:
    result = df.CASE().WHEN('age > 18', 'Adult').WHEN('age >= 13', 'Teen').ELSE('Child').END('age_group')
    """
    return CaseBuilder(df)

@pf.register_dataframe_method
def IF(df, condition, true_value, false_value, column_name):
    """
    Create a simple conditional column (equivalent to a simple CASE statement).

    Parameters:
    df (pd.DataFrame): The DataFrame to apply the condition to.
    condition (str or pd.Series): The condition to evaluate.
    true_value: Value when condition is True.
    false_value: Value when condition is False.
    column_name (str): Name of the new column.

    Returns:
    pd.DataFrame: DataFrame with the new conditional column.
    """
    return CASE(df).WHEN(condition, true_value).ELSE(false_value).END(column_name)
