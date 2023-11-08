import sqlite3
from datetime import datetime


class SQLiteDatabaseConnect:
    def __init__(self, database_name: str):
        self.database_name = database_name
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = """
                CREATE TABLE IF NOT EXISTS records(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    author VARCHAR(50) NOT NULL,
                    description TEXT NOT NULL,
                    creation_date VARCHAR(50) NOT NULL
                )
            """
            cursor.execute(query)
            connection.commit()

    def add_record(self, *, title: str, author: str, description: str):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            values = [title, author, description, datetime.now().strftime('%Y-%m-%d %H:%M')]
            query = """
                INSERT INTO records(title, author, description, creation_date)
                VALUES(?, ?, ?, ?)
            """
            cursor.execute(query, values)
            connection.commit()

    def get_limited_records(self, limit: int = 1000):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            values = [limit, ]
            query = """
                SELECT id, title, author, description, creation_date FROM records
                ORDER BY id DESC
                LIMIT ?
            """
            result = cursor.execute(query, values).fetchall()
            return result

    def get_record_by_search(self, query_str: str):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            search_string = '%' + query_str + '%'
            query = """
                SELECT *
                FROM records
                WHERE 
                    title LIKE :search
                OR 
                    author LIKE :search
                OR
                    description LIKE :search
                ORDER BY id DESC
            """
            result = cursor.execute(query, {'search': search_string})
            return result.fetchall()


database = SQLiteDatabaseConnect('my_records.sqlite3')
