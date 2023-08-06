"""Index and search in a set of documents of different formats.
"""
from . import readers, index


def add_file_to_index(path):
    reader = readers.new('generic')
    tokens = reader.get_tokens(path)
    indexer = index.SimpleIndexer()
    indexer.index(tokens, path)
