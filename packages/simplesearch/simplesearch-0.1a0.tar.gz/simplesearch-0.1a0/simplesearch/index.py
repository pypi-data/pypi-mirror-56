"""Indexation logic for Simple Search."""
from simplesearch import db_helper


class Indexer():
    """Abstract class that defines the set of methods that actual indexers
    need to implement.
    Classes that extends from this should redefine index() which implements
    the way a certain (content, location) pair are indexed.
    """

    def __init__(self):
        raise NotImplementedError("This class shouldn't be instancied.")

    def index(self, content, location):
        raise NotImplementedError


class SimpleIndexer(Indexer):
    """This class implement a simple index which maps values to their
    respective locations.(e.g term 'food' is found under
    ['/home/me/dishes.pdf', '/bin/menu', 'http://food.com']).
    """

    def __init__(self):
        self.db = db_helper.SimpleIndexDB()

    def index(self, values, location):
        """Takes values found under location and reflects that in the index
        for future search.

        Args:
            values: list of terms (e.g lemma, exact term ...)
            location: str representing the location where those values were
            found.
        """
        for value in values:
            self.db.add_location(value, location)
