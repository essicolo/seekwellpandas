import pandas as pd
import pandas_flavor as pf
import re
from functools import lru_cache

# Cache for parsed condition structures to improve performance
@lru_cache(maxsize=128)
def _parse_condition_structure(condition):
    """
    Parse the structure of a condition string and cache the result.
    Returns a tuple containing condition parts and operators for reuse.
    """
    condition_parts = re.split(r'\s+and\s+|\s+or\s+', condition)
    operators = re.findall(r'\s+(and|or)\s+', condition)
    return tuple(condition_parts), tuple(operators)

@lru_cache(maxsize=256)
def _parse_single_condition_structure(cond):
    """
    Parse the structure of a single condition and cache the parsing metadata.
    """
    in_match = re.match(r'(\w+)\s+(not\s+in|in)\s+(.*)', cond)
    if in_match:
        column, op, values = in_match.groups()
        return 'in_operation', column, op, values

    ops = ['==', '!=', '>=', '<=', '>', '<']
    for op in sorted(ops, key=len, reverse=True):
        if op in cond:
            column, value = cond.split(op, 1)  # Split only on first occurrence
            return 'comparison', column.strip(), op, value.strip()

    return 'unknown', None, None, None

@pf.register_dataframe_method
def WHERE(df, condition):
    """
    Filter the DataFrame based on a condition with optimized parsing.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    condition (str): A string representing the condition in SQL-like syntax.

    Returns:
    pd.DataFrame: A filtered DataFrame.
    """
    def parse_value(column, value):
        value = value.strip()
        try:
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
        except KeyError:
            raise ValueError(f"Column '{column}' not found in DataFrame")

    def parse_in_condition(column, values):
        try:
            parsed_values = [parse_value(column, v.strip()) for v in values.split(',')]
            return df[column].isin(parsed_values)
        except KeyError:
            raise ValueError(f"Column '{column}' not found in DataFrame")

    def parse_condition_part(cond):
        condition_type, column, op, value = _parse_single_condition_structure(cond)

        if condition_type == 'in_operation':
            result = parse_in_condition(column, value)
            return ~result if op == "not in" else result
        elif condition_type == 'comparison':
            ops = {
                '==': lambda x, y: x == y,
                '!=': lambda x, y: x != y,
                '>=': lambda x, y: x >= y,
                '<=': lambda x, y: x <= y,
                '>': lambda x, y: x > y,
                '<': lambda x, y: x < y
            }
            try:
                parsed_value = parse_value(column, value)
                if pd.isna(parsed_value):
                    return pd.Series(False, index=df.index)
                return ops[op](df[column], parsed_value)
            except KeyError:
                raise ValueError(f"Column '{column}' not found in DataFrame")
        else:
            return pd.Series(True, index=df.index)

    try:
        condition_parts, operators = _parse_condition_structure(condition)
        parsed_conditions = [parse_condition_part(part) for part in condition_parts]

        final_condition = parsed_conditions[0]
        for i, op in enumerate(operators):
            if op == 'and':
                final_condition = final_condition & parsed_conditions[i+1]
            else:  # 'or'
                final_condition = final_condition | parsed_conditions[i+1]

        return df[final_condition]
    except Exception as e:
        raise ValueError(f"Error parsing WHERE condition '{condition}': {str(e)}")
