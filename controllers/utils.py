import nltk
from newspaper import Article


def clean_articles(articles):
  stop_words= set(stopwords.words('english'))

def parseArticle(url):
  try:
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
  except:
    return "unable to extract from url"

  return text


def checkNltkData():
  modules = ['stopwords','punkt']
  for module in modules:
    try:
      nltk.data.find(module)
    except LookupError:
      nltk.download(module)
    except Exception as e:
      print(str(e))
