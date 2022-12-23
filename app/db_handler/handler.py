import sqlite3
import os


class handler:

    def __init__(self):
        pass

    def db_reader(self, lid: str):

        conn = sqlite3.connect("seen_ids.db")

        cursor = conn.cursor()

        query = 'SELECT * FROM seen_ids WHERE id = ?'
        params = lid

        cursor.execute(query, params)
        cursor.close()

        return cursor.fetchone()

    def db_writer(self, lid: str):

        file = "seen_ids.db"
        conn = sqlite3.connect("seen_ids.db")

        if not os.path.isfile(file):

            conn.execute('''
                CREATE TABLE IF NOT EXISTS seen_ids (
                    id TEXT PRIMARY KEY 
                    )
            ''')
        else:
            cursor = conn.cursor()
            query = 'INSERT INTO seen_ids VALUES (?)'
            params = lid
            cursor.execute(query, params)
            cursor.close()

            return cursor.fetchone()
