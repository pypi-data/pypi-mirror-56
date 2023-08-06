"""Index and search in a set of documents of different formats.
"""
from simplesearch import readers, index, search


def add_file_to_index(path):
    reader = readers.new('generic')
    tokens = reader.get_tokens(path)
    # We only do binary matching, no need for counting tokens
    tokens = list(set(tokens))
    indexer = index.SimpleIndexer()
    indexer.index(tokens, path)


def search_keywords(values: list):
    """Wrapper around search functionalitites.
    """
    return search.search_simple_index(values)
