"""Database helper."""
import sqlite3


FILE_NAME = '.simplesearch.db'
TABLE = 'REVERSE_INDEX'
CREATE = 'CREATE TABLE IF NOT EXISTS {} (lemma unique text, locations)'


class Database():

    def __init__(self, file_name=None):
        if file_name is None:
            file_name = FILE_NAME
        self.connect(file_name)
        self.init_db()

    def connect(self, file_name):
        try:
            self.conn = sqlite3.connect(file_name)

        except sqlite3.Error:
            print("Error connecting to database!")

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute(CREATE.format(TABLE))
        cursor.close()

    def get_locations(self, lemma):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM {} where lemma=?'.format(TABLE), (lemma,))
        result = cursor.fetchall()
        if result:
            # (lemma (unique), locations)
            result = result[0][1]
        else:
            result = None
        cursor.close()
        return result

    def add_location(self, lemma, location):
        cursor = self.conn.cursor()
        insert_query = "INSERT INTO {} VALUES (?,?)".format(TABLE)
        update_query = "UPDATE {} SET locations=? WHERE lemma=?".format(TABLE)

        locations = self.get_locations(lemma)
        if locations is not None:
            if locations:
                locations += ',' + location
            else:
                locations = location
            cursor.execute(update_query, locations, lemma)
        else:
            cursor.execute(insert_query, lemma, location)
        self._commit()
        cursor.close()

    def _commit(self):
        self.conn.commit()
