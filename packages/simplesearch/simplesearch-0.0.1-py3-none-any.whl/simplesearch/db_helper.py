"""Database helper managing the indexes. (sqlite3)"""
import sqlite3


FILE_NAME = '.simplesearch.db'


class Database():
    """Abstract class that defines the set of methods that actual database helper
    need to implement. This classes defines indexes.
    Classes that extends from this should redefine _init_db() which implements
    the way the table for a specific index is created.
    """

    def __init__(self, file_name=None):
        if file_name is None:
            file_name = FILE_NAME
        self._connect(file_name)
        self._init_db()

    def _connect(self, file_name):
        try:
            self.conn = sqlite3.connect(file_name)

        except sqlite3.Error:
            print("Error connecting to database!")

    def _init_db(self):
        """Initialize the index table.
        """
        raise NotImplementedError("Use subclasses of Database.")

    def _commit(self):
        self.conn.commit()


class SimpleIndexDB(Database):
    """Implement simple index storage where locations (e.g documents) are indexed
    using their terms.
    """
    TABLE = 'SIMPLE_INDEX'

    def _init_db(self):
        cursor = self.conn.cursor()
        # locations are comma separated paths (or something equivalent)
        create = 'CREATE TABLE IF NOT EXISTS {} (lemma unique, locations)'
        cursor.execute(create.format(self.TABLE))
        cursor.close()

    def get_locations(self, lemma):
        """Get comma separated locations.
        """
        cursor = self.conn.cursor()
        query = 'SELECT * FROM {} where lemma=?'.format(self.TABLE)
        cursor.execute(query, (lemma,))
        result = cursor.fetchall()
        if result:
            # (lemma (unique), locations)
            result = result[0][1]
        else:
            result = None
        cursor.close()
        return result

    def get_locations_list(self, lemma):
        """Get list of locations.
        """
        locations = self.get_locations(lemma)
        if locations:
            return locations.split(',')
        else:
            return []

    def add_location(self, lemma, location):
        """Add location for a lemma. The lemma is created if not found.
        """
        cursor = self.conn.cursor()
        insert_query = "INSERT INTO {} VALUES (?,?)".format(self.TABLE)
        update_query = "UPDATE {} SET locations=? WHERE lemma=?".format(self.TABLE)

        locations = self.get_locations(lemma)
        if locations is not None:
            if locations:
                locations += ',' + location
            else:
                locations = location
            cursor.execute(update_query, (locations, lemma))
        else:
            cursor.execute(insert_query, (lemma, location))
        self._commit()
        cursor.close()
