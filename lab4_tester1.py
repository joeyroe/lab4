# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 22:06:42 2019

@author: Joey Roe
CS 2302 Data Structures
TA: Anindita Nath, Maliheh Zargaran
Professor: Olac Fuentes
Date: 03/23/2019
Description: work with Btrees, finding minimums or maximums, turning them to lists
             finding the depths as well
"""

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=3):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items


def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
  
           
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
 
           
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
 
     
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()


def IsFull(T):
    return len(T.item) >= T.max_items


def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
  
                
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
    
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
        
#Number2
def treeToList(tree):
    if tree != None:
        if tree.isLeaf == True:      #if the tree is a leaf, the leaf gets returned as a list
            return list(tree.item)
        emptyList = []  #make an empty list to fill up
        for i in range(len(tree.child) - 1):
            tempList = treeToList(tree.child[i])    #make a temporary list
            emptyList = emptyList + tempList + [tree.item[i]]
        lastChildList = treeToList(tree.child[-1])   #this is needed to add the last items
        return emptyList + lastChildList  #return all of the first items with the last items added to them
        

   
#Number 3
def getMinAtDepth(tree, depth):
    if tree != None:
        if depth == 0:
            return tree.item[0]  #returns the very first spot
        if depth > height(tree):  #if the depth exceeds the height it returns -1
            return -1
        else:
            return getMinAtDepth(tree.child[0], depth - 1)
  

      
#Number 4     
def getMaxAtDepth(tree, depth):
    if tree != None:
        if depth == 0:
            return tree.item[-1]   #returns the last spot
        if depth > height(tree):   #this is so the tree returns -1 if the height is exceeded
            return -1
        else:
            return getMaxAtDepth(tree.child[-1], depth - 1) 


 
#Number 5       
def getNumOfNodes(tree, depth):
    if tree != None:
        if depth == 0:
            return 1  #will always be 1 becuase there's only one root node
        if tree.isLeaf:
            return 0
        count = 0 
        for i in range(len(tree.child)):
            count = count + getNumOfNodes(tree.child[i], depth - 1) #adds the number of nodes up
        return count
    



#Number 6      
def printNodes(tree, depth):
    if tree != None:
        if depth == 0:
            print(tree.item, end = '')  #will print nodes once depth is zero
        if depth > height(tree):  #this is for if the depth exceeds the height it prints -1
            print(-1)
        else:
            for i in range(len(tree.child)):   #goes through the tree
                printNodes(tree.child[i], depth - 1)  #subtracts depth till it equals zero
    



#Number 7
def fullNodes(tree):
    if tree != None:
        if len(tree.item) == tree.max_items: #checks to see if length of items list is equal to the max items
            a = 1 #if it is, a is 1
        else:
            a = 0
        for i in range(len(tree.child)):  #goes through the list
            a = a + fullNodes(tree.child[i])  #will add the a's (either 1's or zeros)
        return a   #which returns the number of full nodes


    
    
#Number 8
def fullLeafNodes(tree):
    if tree != None:
        if tree.isLeaf == True:   #checks to see if it's a leaf
            if len(tree.item) == tree.max_items:
                a = 1
            else:
                a = 0
        if tree.isLeaf == False:  #if it's not a leaf, we don't care about it
            a = 0    #so we just set a to 0
            for i in range(len(tree.child)):
                a = a + fullLeafNodes(tree.child[i])
        return a




#Number 9
def FindDepthOfKey(tree,key):
    if tree != None:
        if key in tree.item:
            return 0
        if tree.isLeaf:  #if it's a leaf and not found, key isn't in tree
            return -1
        for i in range(len(tree.child)):
            depth = FindDepthOfKey(tree.child[FindChild(tree, key)],key)  #uses FindChild to find the right child
        if depth == -1:
            return -1     #if depth is -1 key isn't in the tree
        else:
            return depth+1  #adds one to the current depth
        
         
    
 
    
#The Main
L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]
T = BTree()    
for i in L:
    #print('Inserting',i)
    Insert(T,i)
PrintD(T,'') 
    #Print(T)
    #print('\n####################################')
print()   
SearchAndPrint(T,60)
SearchAndPrint(T,200)
SearchAndPrint(T,25)
SearchAndPrint(T,20)
print()

print('height: ', height(T))
print()

theList = treeToList(T)
print('sorted list: ', theList)
print()

a = getMinAtDepth(T, 0)
a1 = getMinAtDepth(T, 1)
a2 = getMinAtDepth(T, 2)
print('min at depth 0: ', a)
print('min at depth 1: ', a1)
print('min at depth 2: ', a2)
print()

b = getMaxAtDepth(T, 0)
b1 = getMaxAtDepth(T, 1)
b2 = getMaxAtDepth(T, 2)
print('max at depth 0: ', b)
print('max at depth 1: ', b1)
print('max at depth 2: ', b2)
print()

print('Number of nodes at depth 0: ', getNumOfNodes(T, 0))
print('Number of nodes at depth 1: ', getNumOfNodes(T, 1))
print('Number of nodes at depth 2: ', getNumOfNodes(T, 2))
print()

print('Nodes at depth 0: ', end = ' ')
printNodes(T, 0)
print()
print('Nodes at depth 1: ', end = ' ')
printNodes(T, 1)
print()
print('Nodes at depth 2:', end = ' ')
printNodes(T, 2)
print()
print()

print('number of full nodes: ', fullNodes(T))
print()

print('number of full leaf nodes: ', fullLeafNodes(T))
print()

print('key 20 is at depth: ', FindDepthOfKey(T, 20))
print('key 800 is at depth: ', FindDepthOfKey(T, 800))