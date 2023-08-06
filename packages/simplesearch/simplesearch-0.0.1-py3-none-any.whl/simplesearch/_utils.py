"""Utilitites for Simple Search."""
from nltk.stem import WordNetLemmatizer
import filetype


def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized = []
    for token in tokens:
        lemmatized.append(lemmatizer.lemmatize(token))
    return lemmatized


def get_file_mime(path_or_bytes):
    kind = filetype.guess(path_or_bytes)
    if kind is None:
        raise Exception("Can't guess filetype")
    return kind.mime
