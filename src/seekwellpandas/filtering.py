import pandas as pd
import pandas_flavor as pf
import re

@pf.register_dataframe_method
def WHERE(df, condition):
    """
    Filter the DataFrame based on a condition.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    condition (str): A string representing the condition in SQL-like syntax.

    Returns:
    pd.DataFrame: A filtered DataFrame.
    """
    def parse_value(column, value):
        value = value.strip()
        column_dtype = df[column].dtype
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
        return df[column].isin(parsed_values)

    def parse_condition(cond):
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
                    return pd.Series(False, index=df.index)
                return ops[op](df[column], parsed_value)

        return pd.Series(True, index=df.index)

    condition_parts = re.split(r'\s+and\s+|\s+or\s+', condition)
    parsed_conditions = [parse_condition(part) for part in condition_parts]

    final_condition = parsed_conditions[0]
    for i, part in enumerate(re.findall(r'\s+(and|or)\s+', condition)):
        if part == 'and':
            final_condition = final_condition & parsed_conditions[i+1]
        else:  # 'or'
            final_condition = final_condition | parsed_conditions[i+1]

    return df[final_condition]
