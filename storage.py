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
                    article_image TEXT NOT NULL,
                    creation_date VARCHAR(50) NOT NULL
                )
            """
            cursor.execute(query)
            connection.commit()

    def add_post(self, *, title: str, author: str, description: str, article_image: str):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            creation_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            values = [title, author, description, article_image, creation_date]
            query = """
                INSERT INTO records(title, author, description, article_image, creation_date)
                VALUES(?, ?, ?, ?, ?)
            """
            cursor.execute(query, values)
            connection.commit()

    def get_posts(self, limit: int = 5):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = """
                SELECT id, title, author, description, article_image, creation_date FROM records
                ORDER BY id DESC
                LIMIT :limit_value
            """
            result = cursor.execute(query, {'limit_value': limit}).fetchall()
            return result

    def get_posts_by_search(self, search_field: str = ''):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            search_string = '%' + search_field + '%'
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

    def get_posts_by_author(self, author: str = ''):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = """
                SELECT *
                FROM records
                WHERE author LIKE :author
                ORDER BY id DESC
            """
            result = cursor.execute(query, {'author': author})
            return result.fetchall()


database = SQLiteDatabaseConnect('my_stories.sqlite3')
