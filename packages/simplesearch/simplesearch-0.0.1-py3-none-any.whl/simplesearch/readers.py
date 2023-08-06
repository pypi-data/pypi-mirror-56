"""Readers implements the logic for extracting tokens from different formats.
"""
import PyPDF2
from nltk.tokenize import word_tokenize
from . import _utils


class FileTypeNotSupported(Exception):
    pass


class Reader():
    """Abstract class that defines the set of methods that actual readers
    need to implement.
    Classes that extends from this should redefine get_text() which implements
    the way the text is extracted for a specific file format.
    """

    def __init__(self):
        pass

    def get_text(self, path, stream=None):
        """Extract text from file found under path. If stream is set
        then read from it without opening the file.

        Args:
            path: path of the file to be parsed.
            stream: readable object.
        Returns:
            raw text.
        """
        return NotImplementedError()

    def get_tokens(self, path, stream=None):
        """Extract tokens from file found under path. If stream is set
        then read from it without opening the file.

        Args:
            path: path of the file to be parsed.
            stream: readable object.
        Returns:
            list of tokens.
        """
        text = self.get_text(path, stream)
        tokens = word_tokenize(text)
        return tokens


class PDF(Reader):
    """PDF file Reader.

    usage example:
    >>> from simplesearch import readers
    >>> pdf_reader = readers.new('pdf')
    >>> pdf_reader.get_text('/home/me/test.pdf')
    'Simple Search'
    >>> pdf_reader.get_tokens('/home/me/test.pdf')
    ['Simple', 'Search']
    """

    def get_text(self, path, stream=None):
        if stream is None:
            stream = open(path, 'rb')

        pdf_reader = PyPDF2.PdfFileReader(stream)
        n_pages = pdf_reader.numPages

        text = ""
        for page_i in range(n_pages):
            page = pdf_reader.getPage(page_i)
            text += page.extractText()

        return text


class GenericReader(Reader):
    """Generic file reader takes any kind of file, try to guess its type
    and use the appropriate Reader class if supported.
    """
    MIME_TO_READER = {
        'application/pdf': PDF,
        }

    def get_text(self, path, stream=None):
        mime = _utils.get_file_mime(path)
        reader_class = self.MIME_TO_READER.get(mime)
        if reader_class is None:
            raise FileTypeNotSupported(mime)
        reader = reader_class()
        return reader.get_text(path)


def new(reader_name):
    """Get reader instance for the wanted format.
    """
    if reader_name == 'pdf':
        return PDF()
    elif reader_name == 'generic':
        return GenericReader()
    return None
