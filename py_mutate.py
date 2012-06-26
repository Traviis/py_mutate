#!/usr/bin/python

#Takes a word
#applies common mutations to it and returns a list of them
#returns a very large set of data 
from leet_table import ltable

def mutate(word,includeOriginal=True,leet=True):
    out = list()
    if includeOriginal:
        out.append(word)
    if leet:
        #do leet mutations
