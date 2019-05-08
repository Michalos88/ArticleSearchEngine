import nltk
from newspaper import Article

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
