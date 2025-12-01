"""
Base Model - Foundation for all database models
Provides common database connection and query methods
"""
import sqlite3


class BaseModel:
    """
    Base class for all models with shared database functionality

    Uses Singleton pattern for database connection management
    All models inherit common CRUD operations
    """

    # Class variable for database path
    DB_PATH = "payroll.db"

    @classmethod
    def set_db_path(cls, path: str):
        """
        Set custom database path (useful for testing)

        Args:
            path: Path to SQLite database file
        """
        cls.DB_PATH = path

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """
        Get database connection with row factory enabled

        Returns:
            sqlite3.Connection: Database connection with dict-like rows
        """
        conn = sqlite3.connect(cls.DB_PATH, timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def execute_query(cls, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """
        Execute a SELECT query and return all results

        Args:
            query: SQL SELECT statement
            params: Query parameters (for prepared statements)

        Returns:
            List of rows as dict-like objects
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    @classmethod
    def execute_single(cls, query: str, params: tuple = ()) -> sqlite3.Row | None:
        """
        Execute a SELECT query and return single result

        Args:
            query: SQL SELECT statement
            params: Query parameters

        Returns:
            Single row as dict-like object, or None if not found
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result

    @classmethod
    def execute_write(cls, query: str, params: tuple = ()) -> int:
        """
        Execute INSERT, UPDATE, or DELETE query

        Args:
            query: SQL write statement
            params: Query parameters

        Returns:
            Number of affected rows
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected

    @classmethod
    def execute_many(cls, query: str, params_list: list[tuple]) -> int:
        """
        Execute batch INSERT/UPDATE operations

        Args:
            query: SQL write statement
            params_list: List of parameter tuples

        Returns:
            Number of affected rows
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.executemany(query, params_list)
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected

    @classmethod
    def get_last_insert_id(cls) -> int | None:
        """
        Get the last inserted row ID

        Returns:
            Last insert rowid, or None if no insert was performed
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
