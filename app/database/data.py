import sqlite3
from sqlite3 import Connection
import os

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
def _get_connection() -> Connection:
    return sqlite3.connect(db_path)

def create_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MouseData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            x_coordinate INTEGER,
            y_coordinate INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ImageData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mouse_data_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            image BLOB,
            FOREIGN KEY (mouse_data_id) REFERENCES MouseData (id)
        )
    ''')

    conn.commit()
    conn.close()



def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)

def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid