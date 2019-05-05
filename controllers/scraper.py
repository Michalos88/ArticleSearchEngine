import time
import logging
from datetime import datetime, timedelta
import requests
import os
import json


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

    self._saveToFile(articles,self.db+'/'+sourceName+'.json')

  def _saveToFile(self,articles,fileName):

    with open(fileName, 'w') as f:
      json.dump(articles, f)

    logging.info('Saved {0} articles'.format(len(articles)))

  def _trendingCall(self,mediaOutletName):

    newsApiKey = os.getenv('news_api_key')
    return ("https://newsapi.org/v2/top-headlines?sources=" + mediaOutletName
      + "&apiKey=" + newsApiKey)


if __name__=='__main__':
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  scraper = NewsScraper('./')
  scraper.getArticles('cnn')