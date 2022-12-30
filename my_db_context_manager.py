import sqlite3


class MyDatabaseContextManager:
    def __init__(self, database):
        self.database = database

    def __enter__(self):
        self.conn = sqlite3.connect(self.database)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise


with MyDatabaseContextManager("database.db") as connection:
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM books")
    print(result.fetchone())
