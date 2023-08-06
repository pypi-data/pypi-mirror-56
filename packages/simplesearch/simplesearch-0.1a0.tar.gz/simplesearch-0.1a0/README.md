# SimpleSearch

SimpleSearch lets you index and search your documents. It was designed to manipulate different types of documents transparently.

#### Note

I developed simplesearch for curiosity reasons, so don't try to run it in production, however, you may find the code helpful as it's well documented.


## Installation

You can install simplesearch using pip

```bash
$ pip install simplesearch
```

or install it from source

```bash
$ git clone https://github.com/youben11/simplesearch
$ cd simplesearch
$ python3 setup.py install
```


## Usage

Simple users will only find two function calls useful, `add_file_to_index()` and `search_keyword()`, those two will allow you to build the index of your documents as well as searching using a list of keywords.

#### Note

Keep in mind that using the `add_file_to_index()` function will create an sqlite3 database file (.simplesearch.db) in your current directory, this same database file will be used for doing search, so doing other operations in another directory will create another index and thus different results.


### Example

Below is a code snippet that index some local files and then do some search operations. Here we used PDFs as it was the only supported document type while writing this example.

```python
import simplesearch

# We assume that this file contains words like
# programming python indexing
simplesearch.add_file_to_index("/home/youben/simplesearch.pdf")

# We assume that this file contains words like
# machine-learning deep-learning python
simplesearch.add_file_to_index("/home/youben/ml.pdf")

# Both files have been indexed now, we can do some search operations

# We searched a specific keyword found only in the second indexed document
simplesearch.search_keywords(["machine-learning"])
['/home/youben/ml.pdf']

# We now do a search on a common keyword for both docs
simplesearch.search_keywords(["python"])
['/home/youben/simplesearch.pdf', '/home/youben/ml.pdf']

# We can also use multiple keywords
simplesearch.search_keywords(["python", "machine-learning"])
['/home/youben/ml.pdf', '/home/youben/simplesearch.pdf']

# The last result was sorted by best match, as the first document matches with two keywods
# while the second match with only one
```

