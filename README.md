# Article Search Engine 

This is a simple implementation of a search engine using Trie data structure as an index holder and TF-IDF for ranking. 
Basically entire vocabulary of words from articles is stored in a Trie, a leaf of each word is and index of the word in occupancy table. 
Occupancy table is python `dict()` aka look-up table that points to uuid's of articles (stored in a db) containing the word from the trie.
Given a query the search engine first finds superset of articles containing any of the words from the query. It then creates a TF-IDF matrix of words in these articles.
Then the program ranks the articles based on the mean TF-IDF scores of query words in each article. 

## Setup
#### Mac OS X

First, set up the virtual environment:

```
pip install virtualenv
virtualenv --python=python3.6 venv
source venv/bin/activate
```

This will create a directory called `venv` in which your virtual
environment lives. The last command activates the environment.

Then, install the dependencies:

```
pip install -r requirements.txt
```

_Note_: In order to source new articles, you need an NewsAPI key, that you can get for free at https://newsapi.org, then:

```
export news_api_key=YOUR_API_KEY
```


## Usage

The entry point to training models:
[`./start.py`](https://github.com/michalos88/ArticleSearchEngine/start.py).
To start the search engine,

```
python start.py
```

This will kick off the program. Input `2` to load the database from file or `3` to build a database of articles.
Then you can search by inputing `1` and your query. 
