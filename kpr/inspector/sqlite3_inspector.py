import sqlite3
import os

class SQLiteDBInspector:
    def __init__(self, db_path):
        """Initialize the class with the path to the SQLite database."""
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False
        return True

    def close(self):
        """Close the connection to the SQLite database."""
        if self.connection:
            self.connection.close()

    def list_tables(self):
        """List all tables in the SQLite database."""
        if not self.connect():
            return
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        self.close()
        return [table[0] for table in tables]

    def table_info(self, table_name):
        """Get the schema information of a specific table."""
        if not self.connect():
            return
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        self.close()
        return columns

    def row_count(self, table_name):
        """Get the row count of a specific table."""
        if not self.connect():
            return
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        self.close()
        return count

    def query(self, query):
        """Execute a custom query on the database."""
        if not self.connect():
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Query failed: {e}")
            self.close()
            return None
        self.close()
        return result

    def db_summary(self):
        """Provide a summary of the database including tables and row counts."""
        tables = self.list_tables()
        if not tables:
            return "No tables found or unable to connect to the database."

        summary = {}
        for table in tables:
            summary[table] = self.row_count(table)
        return summary

