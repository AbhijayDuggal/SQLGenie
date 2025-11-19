import sqlite3
from typing import List, Tuple

def run_sql(db_path: str, sql: str) -> Tuple[List[str], List[Tuple]]:
    """
    Execute a safe SQL query and return column names and rows.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    conn.close()
    return cols, rows
