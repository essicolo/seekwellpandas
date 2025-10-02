"""
Custom exception classes for seekwellpandas that provide SQL-like error messages.
"""

class SQLSyntaxError(Exception):
    """Raised when there's a syntax error in SQL-like conditions."""
    def __init__(self, message, query=None, suggestion=None):
        self.query = query
        self.suggestion = suggestion
        full_message = f"SQL Syntax Error: {message}"
        if query:
            full_message += f"\nQuery: {query}"
        if suggestion:
            full_message += f"\nSuggestion: {suggestion}"
        super().__init__(full_message)

class ColumnNotFoundError(Exception):
    """Raised when a referenced column doesn't exist."""
    def __init__(self, column_name, available_columns=None, suggestion=None):
        self.column_name = column_name
        self.available_columns = available_columns
        message = f"Column '{column_name}' not found"
        if available_columns:
            message += f"\nAvailable columns: {', '.join(available_columns)}"
        if suggestion:
            message += f"\nDid you mean: {suggestion}?"
        super().__init__(message)

class InvalidJoinError(Exception):
    """Raised when join parameters are invalid."""
    def __init__(self, message, suggestion=None):
        full_message = f"Join Error: {message}"
        if suggestion:
            full_message += f"\nSuggestion: {suggestion}"
        super().__init__(full_message)

class AggregationError(Exception):
    """Raised when aggregation operations fail."""
    def __init__(self, message, operation=None, suggestion=None):
        full_message = f"Aggregation Error: {message}"
        if operation:
            full_message += f"\nOperation: {operation}"
        if suggestion:
            full_message += f"\nSuggestion: {suggestion}"
        super().__init__(full_message)

def suggest_column_name(target, available_columns, max_suggestions=3):
    """
    Suggest similar column names using basic string similarity.
    """
    import difflib
    suggestions = difflib.get_close_matches(target, available_columns, n=max_suggestions, cutoff=0.6)
    return suggestions

def validate_columns_exist(df, columns, operation_name="operation"):
    """
    Validate that all specified columns exist in the DataFrame.
    Raises ColumnNotFoundError with suggestions if any column is missing.
    """
    if isinstance(columns, str):
        columns = [columns]

    missing_columns = []
    for col in columns:
        if col not in df.columns:
            missing_columns.append(col)

    if missing_columns:
        for missing_col in missing_columns:
            suggestions = suggest_column_name(missing_col, df.columns.tolist())
            suggestion = suggestions[0] if suggestions else None
            raise ColumnNotFoundError(
                missing_col,
                df.columns.tolist(),
                suggestion
            )
