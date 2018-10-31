# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
import sys
from textblob import TextBlob
from textblob import Word
from collections import defaultdict

uselessTerm = ["username","text","tweetid"]
postings = defaultdict(dict)


def merge2_and(term1,term2):
    global postings
    if (term1 not in postings) or (term2 not in postings):
        print("not find!")
        return
#    else:
#        posyings[term1][]

def merge2_or(term1,term2):
    return 0

def merge2_not(term1,term2):
    return 0

def token(doc):
    doc = doc.lower()
    terms=TextBlob(doc).words.singularize()
    
    result=[]
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")     
        result.append(expected_str)
    return result         

def tokenize_tweet(document):
    
    document=document.lower()
    a = document.index("username")
    b = document.index("clusterno")
    c = document.rindex("tweetid")-1
    d = document.rindex("errorcode")
    e = document.index("text")
    f = document.index("timestr")-3  
    document = document[c:d]+document[a:b]+document[e:f]
    terms=TextBlob(document).words.singularize()
      
    result=[]
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")
        if expected_str not in uselessTerm:
            result.append(expected_str)
    return result


def get_postings():
    
    global postings
    f = open(r"C:\Users\93568\Documents\GitHub\DataMining\work3Inverted index and Boolean Retrieval Model\0123.txt")  
    lines = f.readlines()#读取全部内容

    for line in lines:
       line = tokenize_tweet(line)
       tweetid = line[0]
       #print(tweetid)
       line.pop(0);
       unique_terms = set(line)
       for te in unique_terms:
           if te in postings:                         
               postings[te].append(tweetid)           
           else:            
               postings[te] = [tweetid]
    #按字典序对postings进行升序排序
    postings = sorted(postings.items(),key = lambda asd:asd[0],reverse=False)       
    print(len(postings))
    
    
def do_search():
    terms = token(input("Search query >> "))
    if terms == []:
        sys.exit()
    
    if len(terms)==3:
        if terms[1]=="and":
            merge2_and(terms[0],terms[2])
            return "going well! and2"
        elif terms[1]=="or":
            merge2_or(terms[0],terms[2])
            return "going well! or2"
        elif terms[1]=="not":
            merge2_not(terms[0],terms[2])
            return "going well! not2"
        else:
            return "input wrong!"
        
    elif len(terms)==5:
        return "going well!"
    
    

def main():
    get_postings()
    #while True:
        #print(do_search())


if __name__ == "__main__":
    main()
