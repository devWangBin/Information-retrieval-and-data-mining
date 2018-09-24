# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 11:46:14 2018

@author: 93568
"""
import math
import ast
from collections import Counter
wordsCount=0#variable for wordsfrequency
def CountKeyByWen(fileName1):
    global wordsCount
    f1=open(fileName1,'rb')
    f2=open(fileName2,'rb')
    table={}
    for lines in f1:
        for line in lines.split(' '.encode(encoding="utf-8")):
            if line!=' ' and line in table:
                table[line]+=1
                wordsCount+=1
            elif line!=' ':
                wordsCount+=1
                table[line]=1
    #dic = sorted(table.iteritems(),key= lambda asd:asd[1], reverse=True)
    # print len(dic) code for testing
    return table
# seconde:create vocabulary
def CreateVocabulary(dic1=None, dic2=None):
    vocabulary=[]
    for dicEle in dic1:
        if dicEle not in vocabulary:
            vocabulary.append(dicEle)
    for dicEle in dic2:
        if dicEle not in vocabulary:
            vocabulary.append(dicEle)
    # print len(vocabulary) code for testing
    return vocabulary
# third:compute TF-IDF output: a vector
# In this code we just use TF for computing similarity
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs],[]))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([obj.get(_key,0) for obj in objs])
    return _total
def ComputeVector(dic1=None,vocabulary=None):
    # 3.1compute cipin global wordscount wordsCount
    # 3.2create vector
    dicVector = {}
    for elem in vocabulary:
        dicVector[elem]=0
    # dicVector = sorted(dicVector.iteritems(),key= lambda asd:asd[1], reverse=True)
    # U"vocabulary --->dicVector"
    # U"dic1->vector"
    dicTemp=union_dict(dicVector,dic1);
    # dicTemp1,dicTemp2=Counter(dicVector), Counter(dic1)
    # dicTemp=dict(dicTemp1+dicTemp2)
    # dicTemp = sorted(dicTemp.iteritems(),key= lambda asd:asd[1], reverse=True)
    return  dicTemp
# fourth: compute TF-IDF
def ComputeSimlirity(dic1Vector=None,dic2Vector=None):
    x=0.0 #fenzi
    #fenmu
    y1=0.0
    y2=0.0
    for k in dic1Vector:# because of the element of dic1 and dic2 are the same
        temp1=(float)(float(dic1Vector[k])/float(wordsCount))
        temp2=(float)(float(dic2Vector[k])/float(wordsCount))
        x=x+ (temp1*temp2)
        y1+=pow(temp1,2)
        y2+=pow(temp2,2)
    return x/math.sqrt(y1*y2)

if __name__=='__main__':
    fileName1='01.txt';
    fileName2='02.txt';
    dic1 = CountKeyByWen(fileName1)
    dic2 = CountKeyByWen(fileName2)
    vocabulary = CreateVocabulary(dic1, dic2)
    dic1Vector = ComputeVector(dic1, vocabulary)
    dic2Vector = ComputeVector(dic2, vocabulary)
    for elem in dic1Vector:
        print ("<"+elem,',',str(dic1Vector[elem])+">")
    sim=ComputeSimlirity(dic1Vector,dic2Vector)
    print ("similarity="+str(sim))
    #####################################