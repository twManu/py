#!/usr/bin/python

"""
Assign functions to variables
"""
def greet(name):
    return "hello "+name

greet_someone = greet
print greet_someone("John")

