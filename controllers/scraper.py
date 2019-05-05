import time
import logging
from datetime import datetime, timedelta
from controllers.utils import parseArticle
import requests
import os
import json
import uuid

class NewsScraper():
  def __init__(self,
              db=None):
    self.db = db

  def getArticles(self,sourceName):

    logging.info('Getting {0} articles'.format(sourceName))
    try:
      r = requests.get(self._trendingCall(sourceName))
      articles = r.json()['articles']
    except Exception as e:
      articles = []
      logging.warning("getArticles/crashed")
      logging.error(str(e))
    for article in articles:
      article['content'] = parseArticle(article['url'])
      article['_id'] = str(uuid.uuid4())
      self._saveToFile(article)
    return articles

  def _saveToFile(self,article):
    with open(self.db+'/'+str(article['_id'])+'.json', 'w') as f:
      json.dump(article, f)

  def _trendingCall(self,mediaOutletName):

    newsApiKey = os.getenv('news_api_key')
    return ("https://newsapi.org/v2/top-headlines?sources=" + mediaOutletName
      + "&apiKey=" + newsApiKey)


if __name__=='__main__':
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  scraper = NewsScraper('./')
  scraper.getArticles('cnn')