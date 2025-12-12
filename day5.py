class Node:

    def __init__(self,low,high,maximum,parent=None,left=None,right=None, isRed=True):
      self.low = low
      self.high = high
      self.maximum = maximum
      self.parent = parent
      self.left = left
      self.right = right
      self.isRed = isRed

class RedBlackIntervalTree:

    def __init__(self):
      self.nil = Node(None,None,None,None,None,None,False)
      self.root = self.nil


    def toList(self) -> tuple[int,int]:
      
      intervals = []
      self._toListHelper(self.root,intervals)
      return intervals

    def _toListHelper(self,node,intervals):
      if node.left != self.nil:
        self._toListHelper(node.left,intervals)

      intervals.append((node.low,node.high))

      if node.right != self.nil:
        self._toListHelper(node.right,intervals)

    def contains(self, key) -> Node:
      node = self.root
      while node != self.nil and not (key >= node.low and key <= node.high):
        if node.left != self.nil and key <= node.left.maximum:
          node = node.left
        else:
          node = node.right

      if node == self.nil:
        return False
      else:
        return True

    def rotateLeft(self, subRoot):

      subRootRight = subRoot.right

      subRoot.right = subRootRight.left
      if subRootRight.left != self.nil:
        subRootRight.left.parent = subRoot

      subRootRight.parent = subRoot.parent
      if subRoot.parent == self.nil:
        self.root = subRootRight
      elif subRoot.parent.left == subRoot:
        subRoot.parent.left = subRootRight
      else:
        subRoot.parent.right = subRootRight

      subRootRight.left = subRoot
      subRoot.maximum = max(subRoot.high,subRoot.right.maximum or -1,subRoot.left.maximum or -1)
      subRootRight.maximum = max(subRootRight.high,subRootRight.right.maximum or -1,subRootRight.left.maximum or -1)
      subRoot.parent = subRootRight

    def rotateRight(self, subRoot):

      subRootLeft = subRoot.left

      subRoot.left = subRootLeft.right
      if subRootLeft.right != self.nil:
        subRootLeft.right.parent = subRoot

      subRootLeft.parent = subRoot.parent
      if subRoot.parent == self.nil:
        self.root = subRootLeft
      elif subRoot.parent.right == subRoot:
        subRoot.parent.right = subRootLeft
      else:
        subRoot.parent.left = subRootLeft

      subRootLeft.right = subRoot
      subRootLeft.maximum = max(subRootLeft.high,subRootLeft.left.maximum or -1, subRootLeft.right.maximum or -1)
      subRoot.parent = subRootLeft

    def insert(self,low,high):

      current = self.root
      insertParent = self.nil
      while current != self.nil:
        insertParent = current
        if low == current.low:
          current.maximum = max(current.maximum or -1, high)
          current.high = max(current.high, high)
          return
        elif low < current.low:
          current = current.left 
        else:
          insertParent.maximum = max(insertParent.maximum or -1, high)
          current = current.right
      
      insertNode = Node(low,high,high,insertParent,self.nil,self.nil)

      if insertParent == self.nil:
        self.root = insertNode
      elif insertParent.low > low:
        insertParent.left = insertNode
      else:
        insertParent.right = insertNode

      self.fixInsert(insertNode)

    def fixInsert(self,insertNode):

      if insertNode == self.root:
        if self.root.isRed:
          self.root.isRed = False
        return

      parent = insertNode.parent

      if parent == self.root:
        self.fixInsert(parent)
        return

      grandparent = parent.parent
      uncle = None
      if grandparent.left == parent:
        uncle = grandparent.right
      else:
        uncle = grandparent.left

      if uncle.isRed:
        parent.isRed = False
        uncle.isRed = False
        grandparent.isRed = True
        self.fixInsert(grandparent)
        return
      
      if parent == grandparent.left:
        if insertNode == parent.left:
          parent.isRed = False
          grandparent.isRed = True
          self.rotateRight(grandparent)
        else:
          self.rotateLeft(parent)
          insertNode.isRed = False
          grandparent.isRed = True
          self.rotateRight(grandparent)
      else:
        if insertNode == parent.left:
          self.rotateRight(parent)
          insertNode.isRed = False
          grandparent.isRed = True
          self.rotateLeft(grandparent)
        else:
          parent.isRed = False
          grandparent.isRed = True
          self.rotateLeft(grandparent)
      
input = """"""

rangesAndIngredients = input.splitlines()

ranges = []
ingredients = []

isRange = True
for rAndI in rangesAndIngredients:
  if not rAndI:
    isRange = False
    continue
  
  if isRange:
    ranges.append(rAndI)
  else:
    ingredients.append(rAndI)

intervals = RedBlackIntervalTree()

for r in ranges:
  low,high = r.split("-")
  intervals.insert(int(low),int(high))


output = 0

for i in ingredients:
  if intervals.contains(int(i)):
    output += 1

print("Solution 1: " + str(output))

orderedIntervals = intervals.toList()
low = orderedIntervals[0][0]
high = orderedIntervals[0][1]
midLow = high

output = 0

for i,interval in enumerate(orderedIntervals[1:]):
  if i == len(orderedIntervals)-2:
    if interval[0] < high:
      output += (interval[1] - low) + 1
    else:
      output += (interval[1] - interval[0]) + 1 + (high - low) + 1
  elif interval[1] <= high and interval[0] >= low:
    continue
  elif interval[1] >= high >= interval[0]:
    high = interval[1]
  else:
    output += (high - low) + 1
    high = interval[1]
    midLow = low
    low = interval[0]

print("Solution 2: " + str(output))