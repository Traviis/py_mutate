#!/usr/bin/python

#Takes a wordlist
#applies common mutations to each word and returns a list of them
#single words can return upwords of >2000 results depending on settings.
from leet_table import ltable
import sys
import operator
import math
import itertools


def bin_string_with_pad(s,leng=1):
    sv = s if s<=1 else bin_string_with_pad(s>>1) + str(s&1)
    return ("{0:0" + str(leng) + "d}").format(int(sv))

def getLeet(word,runcaps=True):
#This needs to be cleaned up; currently it generates every single possible table 
    def generate_tables(ltable):
        keys = sorted(ltable.keys()) 
        cur_table = dict()
        list_of_lists = list()
        for key in keys:
           needed_len = len(ltable[key.upper()])
           list_of_lists.append([x for x in range(0,needed_len)])
        vals = list(itertools.product(*list_of_lists))
        return vals

    def get_cur_table(curset,ltable):
        keys = sorted(ltable.keys()) # not really neccisary
        cur_table = dict()
        for key_idx in range(0,len(curset)):
            cur_table[keys[key_idx]] = ltable[keys[key_idx].upper()][curset[key_idx]]
        return cur_table

    dictpos = reduce(operator.mul,[len(ltable[x]) for x in ltable if len(ltable[x]) > 0],1)
    outset = set()
    y = 0
    gen = generate_tables(ltable)
    while y < dictpos: #dictpos was too big for range in some cases
        curset = gen[y]
        cur_table = get_cur_table(curset,ltable)
        maxn = int(math.pow(2,len(word)))
        x = 0
        #for x in range(0,int(math.pow(2,len(word)))):
        while x < maxn:
           newword = word
           bset = bin_string_with_pad(x,len(word))
           for i in range(0,len(bset)):
                up_w1 = word[i].upper()
                if bset[i] == '1' and up_w1 in cur_table.keys():
                    newword = newword[0:i] + cur_table[up_w1] + newword[i+1:]
                    outset.add(newword)
                    if runcaps:
                        for capped in getCaps(newword):
                            outset.add(capped)
           x += 1
        y += 1
    return list(outset)

def getCaps(word):
    #Get all upper and lower case possibilities
    out = set()
    lower = word.lower()
    x = 0
    maxx = int(math.pow(2,len(word)))
    #for x in range(0,int(math.pow(2,len(word)))):
    while x < maxx: 
        bset = bin_string_with_pad(x,len(word))
        #1's are caps, 0's are lower
        newword = ''
        for i in range(0,len(bset)):
            if bset[i] == '1':
               newword += word[i].upper()
            else:
                newword += word[i]
        x += 1
        out.add(newword)
    return out
        


def mutate(word,includeOriginal=True,leet=True,caps=True,numbers=True):
    out = set()
    if includeOriginal:
        out.add(word)
    if leet:
        for x in getLeet(word):
            out.add(x)
    if caps:
        for x in getCaps(word):
            out.add(x)
    if numbers:
        for x in addnumbers(word):
            out.add(x)
    return out

def addnumbers(word,prefix=True,postfix=True,maxnumber=1000): #common for birthyears
       out = set()
       if prefix:
            for n in range(0,maxnumber):
                out.add(str(n)+word)
       if postfix:
            for n in range(0,maxnumber):
                out.add(word+str(n))
       if postfix and prefix:
          lists = [ [x for x in range(maxnumber)],[x for x in range(maxnumber)] ] 
          all_combo = itertools.product(*lists)
          print all_combo
       return out

#default operation is to read the file in sys.stdin and print out all the mutations (per word)
if len(sys.argv) > 1:
    if sys.argv[1] == '-':
        #stdin
        f = sys.stdin
    else:
        f = open(sys.argv[1],'r')
    for line in f:
        for word in mutate(line.split('\n')[0]):
            print word
else:
    print "Supply wordlist as the first arguement"
