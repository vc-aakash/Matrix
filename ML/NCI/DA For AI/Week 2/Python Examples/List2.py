#!/usr/bin/env python
# coding: utf-8

# In[24]:


fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
fruits.count('apple')

fruits.append('grapes')

fruits.count('tangerine')

fruits.index('banana')

fruits.index('banana', 4)  # Find next banana starting a position 4

fruits.reverse()

#fruits.append('grapes')

fruits.insert(3, 'cherry')

fruits.remove('cherry')

fruits.sort()
fruits

fruits.pop()
fruits
fruits.pop(3)

f = fruits
f
print(type(f))


# In[27]:


#List as stack

stack = [3, 4, 5]
stack.append(6)
stack.append(7)
stack

stack.pop()
stack


# In[30]:


#list as queue

from collections import deque

queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")           # Terry arrives
queue.append("Graham")          # Graham arrives
queue.popleft()                 # The first to arrive now leaves
queue.popleft()                 # The second to arrive now leaves

queue                 


# In[ ]:




