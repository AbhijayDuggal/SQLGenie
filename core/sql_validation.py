def is_safe_sql(sql: str) -> bool:
    """Simple safety check for SQL queries."""
    sql_lower = sql.lower()
    forbidden = ["drop", "delete", "update", "alter"]
    return not any(word in sql_lower for word in forbidden)
