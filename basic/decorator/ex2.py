#!/usr/bin/python

"""
Functions can be passed as parameters to other functions
"""

def greet(name):
   return "Hello " + name 

def call_func(func):
    other_name = "John"
    return func(other_name)  

print call_func(greet)

