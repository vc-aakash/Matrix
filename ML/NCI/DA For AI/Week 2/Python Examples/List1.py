#!/usr/bin/env python
# coding: utf-8

# In[32]:


squares = [1, 4, 9, 16, 25]
squares


# In[29]:


list([1,2,3,4])
list()
list("abcdef")
#squares[3]


# In[3]:


squares[-3:]  # slicing returns a new list
[9, 16, 25]


# In[17]:


myList = range(1,11)
print(len(myList))
list(range(0, 10, 3))
list(range(-10, -100, -30))


# In[19]:


squares[:] #shallow copy


# In[28]:


myList1 = range(1,11)
print(len(myList1))
print(min(myList1))
print(max(myList1))
print(sum(myList1)) 

myList2 = ['f','a','c','d','d','e','c','b','g']
print(myList2.index('f'))
print(myList2.count('f'))
myList.sort()
print(myList)


# In[31]:


odd30 = [ x for x in range(31) if x % 2 == 1]
print(odd30)

even30 = [ x for x in range(31) if x % 2 == 0]
print(even30)


# In[33]:


squares + [36, 49, 64, 81, 100]


# In[39]:


cubes = [1, 8, 27, 65, 125]

cubes[3]=64

cubes.append(216)  # add the cube of 6
cubes.append(7 ** 3)  # and the cube of 7
cubes


# In[47]:


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
#letters[2:5] = ['C', 'D', 'E']
#letters[2:5] = []
#letters[:] = []
letters
#len(letters)


# In[50]:


list2d = [cubes,letters]
list2d
list2d[1]
list2d[1][2]


# In[55]:


# Fibonacci series:
# the sum of two elements defines the next
a, b = 0, 1
while a < 10:
    print(a, b)
    #print(a, end=', ')
    a, b = b, a+b


# In[ ]:




