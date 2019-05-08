from controllers.trie import Trie
from controllers.utils import checkNltkData
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import pandas as pd
import logging
import numpy as np
import re

checkNltkData()
stopWords = stopwords.words('english')

class SearchEngine:
  def __init__(self,
              trie=Trie(),
              occupancy=dict(),
              db='./db/'):
    self.trie = trie
    self.occupancy = occupancy
    self.db = db

  def addPages(self, pages):
    for page in pages:
      words = self._cleanText(page['content'])
      for word in words:
        idx = self.trie.addChild(word)
        try:
          self.occupancy[idx].append(page['_id'])
        except:
          self.occupancy[idx] = [page['_id']]

  ### TODO: DECIDE IF YOU WANT TO GIVE ARTICLES WITH HALF QUERY
  def query(self, query):
    selectedIds = list()
    words = self._cleanText(query)
    words = list(set(words))
    putativeMatches = list()
    for word in words:
      idx = self.trie.getIndex(word)
      if idx is not None:
       putativeMatches.extend(self.occupancy[idx])

    uniqueMatches = list(set(putativeMatches))
    for match in uniqueMatches:
      if putativeMatches.count(match) >= len(words):
        selectedIds.append(match)
    if len(selectedIds)>0:
      pages = self._retrieveDocuments(selectedIds).dropna(axis=0)
      texts = pages['content'].values.tolist()
      pages['ranking'] = self._rank(texts, words)
      pages = pages.sort_values('ranking',ascending=False)
      for i in range(0,len(pages.index.tolist()),1):
        if i < 6:
          page = pages.iloc[i]
          print("##########################")
          print("Title:",page['title'])
          print("Author:",page['author'])
          print("Source:",page['source']['name'])
          print("Excerpt:",page['content'][0:350])
          print("Relevancy Score:",round(page['ranking']*100,2))
        else:
          break
    else:
      print('No Pages Matching The Query')

  def _retrieveDocuments(self, ids):
    pages = list()
    for id_ in ids:
      try:
        with open(self.db+id_+'.json','r') as f:
          pages.append(json.load(f))
      except:
        logging.error("Can't Find Document with id",id_)

    return pd.DataFrame(pages)

  def _rank(self, documents, words):
    tfidfVectorizer = TfidfVectorizer()
    tfidfMatrix = tfidfVectorizer.fit_transform(documents)
    tfidfMatrix = tfidfMatrix.toarray()
    ranking = np.zeros((len(documents),1))
    for word in words:
      if word in tfidfVectorizer.vocabulary_.keys():
        idx = tfidfVectorizer.vocabulary_[word]
        ranking+=tfidfMatrix[:,idx].reshape(-1,1)
    ranking = ranking/len(documents)
    return ranking

  def _cleanText(self, text):
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