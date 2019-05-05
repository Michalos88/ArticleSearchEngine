class _Root:
  def __init__(self):
      self.children = dict()

class Trie:

  def __init__(self):
    """Initialises the trie"""
    self._root = _Root()
    self.top_index = 0

  def isEmpty(self):
    """Checks if the trie is empty"""
    if len(self._root.children.keys()) == 0:
      return True
    else:
      return False

  def addChild(self, word):
    """Adds word to the Trie"""
    node = self._root.children
    for char in word.lower():
      if char in node.keys():
        node = node[char]
      else:
        node[char] = {}
        node = node[char]
    try:
      return node['__index__']
    except KeyError:
      node['__index__'] = self.top_index
      self.top_index+=1
      return node['__index__']

  def getIndex(self, word):
    """Gets index of a word in Trie"""
    node = self._root.children
    for char in word.lower():
      if char in node.keys():
        node = node[char]
      else:
        return None
    try:
      return node['__index__']
    except KeyError:
      return None

  def show(self):
    """Prints entire trie."""
    print(self._root.children)

  def copy(self):
    """Returns a copy of the trie."""
    return self.__class__(self)


if __name__ == "__main__":
  data = Trie()
  x = data.addChild('lol')
  y = data.addChild('lol2')
  z = data.addChild('lol2')
  print(x,y,z)
  print(data.getIndex('lol2'))
  data.show()