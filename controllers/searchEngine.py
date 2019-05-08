from controllers.trie import Trie
from controllers.utils import checkNltkData
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import TfidfVectorizer

import logging
import re

checkNltkData()
stopWords = stopwords.words('english')

class SearchEngine:
  def __init__(self,
              trie=Trie(),
              occupancy=dict()):
    self.trie = trie
    self.occupancy = occupancy

  def addPages(self, pages):
    for page in pages:
      words = self._clean_text(page['content'])
      for word in words:
        idx = self.trie.addChild(word)
        try:
          self.occupancy[idx].append(page['_id'])
        except:
          self.occupancy[idx] = [page['_id']]

  ### TODO: DECIDE IF YOU WANT TO GIVE ARTICLES WITH HALF QUERY
  def query(self, query):
    output = list()
    words = word_tokenize(query)
    words = list(set(words))
    putativeMatches = list()
    for word in words:
      idx = self.trie.getIndex(word)
      if idx is not None:
       putativeMatches.extend(self.occupancy[idx])

    uniqueMatches = list(set(putativeMatches))
    for match in uniqueMatches:
      if putativeMatches.count(match) >= len(words):
        output.append(match)
    return output

  def _retrieve_documents(self, ids):
    pages = list()
    pass

  def _rank(self, pages):
    pass

  def _clean_text(self, text):
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    tags = re.findall(r'#\w+\b', text)
    emojis = re.findall(r'[^\x00-\x7F]', text) # TODO: Sometimes UTF's are not emojis like '
    questionMarks = re.findall(r'\?',text)

    # Remove non-words
    text = self._removeAll(links, text)
    text = self._removeAll(emojis, text)
    text = self._removeAll(tags, text)

    allWords = re.findall(r'[a-zA-Z\']+', text)

    allWordsCount = len(allWords)

    # Getting rid of stop words and 1 letter words
    meaningfulWords = []
    for word in allWords:
      if len(word) > 1:
        # Standard word in the database has to be in lower cap
        word = word.lower()
        if not word in stopWords:
          meaningfulWords.append(word)

    return meaningfulWords

  def _removeAll(self, nonWords, text):
    for nonWord in nonWords:
      text = text.replace(nonWord, "")
    return text

if __name__ == "__main__":
  se = SearchEngine()
  se.addPages(['dsfs JDFjsdlfkjsadlfjasd flsdaflsjflasd'])