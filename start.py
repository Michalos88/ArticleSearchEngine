from controllers.scraper import NewsScraper
from controllers.searchEngine import SearchEngine
import logging
import pickle
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""Constants"""
DB = './db/'
SOURCES = ['cnn','cnbc','bloomberg','fox-news','techcrunch','msnbc',
                  'abc-news','espn','financial-post','fox-sports','mashable',
                  'new-york-magazine','recode','the-economist']

se = SearchEngine()

run=True
while run:
  print("########## Menu ##########")
  print("1: Search")
  print("2: Load the Database From File")
  print("3: Build New Database (requires NewsApi Key)")
  print("4: Get Statistics")
  print("5: Save State")
  print("6: Exit")
  selection = input("Your Choice: ")
  print("##########################")

  if selection=='1':
    if not se.trie.isEmpty():
      searchQuery = input('Your Query: ')
      se.query(searchQuery)
    else:
      print('The Search Engine is empty!')
      print('Load or Build the DataBase!')
  elif selection == '2':
    try:
      with open('searchEngine_state.pkl','rb') as f:
        seLoad = pickle.load(f)
        se.trie = seLoad.trie
        se.occupancy = seLoad.occupancy
        # se.db = se_load.db
      print('SearchEngine State Loaded')
    except FileNotFoundError:
      print('Search Engine State Not Found')
  elif selection == '3':
    logging.info('Building DataBase')
    scraper = NewsScraper(db=DB)
    for source in SOURCES:
      articles = scraper.getArticles(source)
      se.addPages(articles)
  elif selection =='4':
    if not se.trie.isEmpty():
      print("Number of words in Search Engine:",se.trie.topIndex)
    else:
      print('The Search Engine is empty!')
      print('Load or Build the DataBase!')
  elif selection=='5':
    try:
      with open('searchEngine_state.pkl','wb') as f:
        pickle.dump(se,f)
      print('SearchEngine State Saved')
    except:
      print('Error Occured while saving')
  elif selection=='6':
    run=False