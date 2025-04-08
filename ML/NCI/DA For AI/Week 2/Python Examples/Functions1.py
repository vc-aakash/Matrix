#!/usr/bin/env python
# coding: utf-8

# In[7]:


def fib(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()
        
 # Now call the function we just defined:
fib(2000)
fib(3000)
fib
f = fib(100)
f


# In[5]:


def fib2(n):  # return Fibonacci series up to n
    """Return a list containing the Fibonacci series up to n."""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)    # see below
        a, b = b, a+b
    return result

f100 = fib2(100)    # call it
f100                # write the result


# In[5]:


a = "Data Analytics"
b = "Students"
c = "Hello {} {}"
print(c.format(b,a))


# In[4]:


#Arguments

def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)


# In[11]:


#default values at fun definition

i = 5

def f(arg=i):
    print(arg)

i = 6
f()


# In[12]:


def f(a, L=[]):
    L.append(a)
    return L

print(f(1))
print(f(2))
print(f(3))


# In[16]:


def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L

print(f(1))
print(f(2))
print(f(3))


# In[26]:


#keyword arguments

def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")

#valid
parrot(1000)                                          # 1 positional argument
#parrot(voltage=1000)                                  # 1 keyword argument
#parrot(voltage=1000000, action='VOOOOOM')             # 2 keyword arguments
#parrot(action='VOOOOOM', voltage=1000000)             # 2 keyword arguments
#parrot('a million', 'bereft of life', 'jump')         # 3 positional arguments
#parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword

#invalid
#parrot()                     # required argument missing
#parrot(voltage=5.0,'dead')  # non-keyword argument after a keyword argument
#parrot(110, voltage=220)     # duplicate value for the same argument
#parrot(actor='John Cleese')  # unknown keyword argument


# In[27]:


def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])
        
cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")


# In[3]:


#lambda

def make_incrementor(n):
    return lambda x: x + n

f = make_incrementor(42)
f(0)

pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five')]
pairs.sort(key=lambda pair: pair[1])
pairs


# In[ ]:




