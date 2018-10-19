# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:38:14 2018
@author: WB
"""
from textblob import TextBlob
from textblob import Word
from collections import defaultdict
import math
import os
import re

doc1_filenames={}
doc2_filenames={}
doc3_filenames={}
doc4_filenames={}
doc5_filenames={}
# postings[term] 表示在类别内term词的词频
postings1 = defaultdict(dict)
postings2 = defaultdict(dict)
postings3 = defaultdict(dict)
postings4 = defaultdict(dict)
postings5 = defaultdict(dict)
#每个类别的总词数
num_c1=0
num_c2=0
num_c3=0
num_c4=0
num_c5=0

total_aRate=0

def main():
    Newspath1=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_test\alt.atheism")
    Newspath2=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_test\comp.graphics")
    Newspath3=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_test\rec.sport.hockey")
    Newspath4=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_test\comp.sys.ibm.pc.hardware")
    Newspath5=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_test\comp.sys.mac.hardware")
    getClass_dic()
    initialize_terms_and_postings()
    #print(len(postings1),len(postings2),len(postings3),len(postings4),len(postings5))
    test(Newspath1,0)
    test(Newspath2,1)
    test(Newspath3,2)
    test(Newspath4,3)
    test(Newspath5,4)
    print("平均准确率为：",total_aRate/5)
    
def initialize_terms_and_postings():
    global postings1,postings2,postings3,postings4,postings5,num_c1,num_c2,num_c3,num_c4,num_c5
    for id in doc1_filenames:
        f = open(doc1_filenames[id],'r',encoding='utf-8',errors='ignore')
        document = f.read()
        f.close()
        terms = tokenize(document)
        num_c1+=len(terms)#类1总词数
        unique_terms = set(terms)
        for term in unique_terms:
            if term not in postings1:
                postings1[term] = (terms.count(term))
            else:
                postings1[term] =(postings1[term]+(terms.count(term)))
    
    
    for id in doc2_filenames:
        f = open(doc2_filenames[id],'r',encoding='utf-8',errors='ignore')
        document = f.read()
        f.close()
        terms = tokenize(document)
        num_c2+=len(terms)#类2总词数
        unique_terms = set(terms)
        for term in unique_terms:
            if term not in postings2:
                postings2[term] = (terms.count(term))
            else:
                postings2[term] =(postings2[term]+(terms.count(term)))
    
   
    for id in doc3_filenames:
        f = open(doc3_filenames[id],'r',encoding='utf-8',errors='ignore')
        document = f.read()
        f.close()
        terms = tokenize(document)
        num_c3+=len(terms)#类3总词数
        unique_terms = set(terms)
        for term in unique_terms:
            if term not in postings3:
                postings3[term] = (terms.count(term))
            else:
                postings3[term] =(postings3[term]+(terms.count(term)))
                
    
    for id in doc4_filenames:
        f = open(doc4_filenames[id],'r',encoding='utf-8',errors='ignore')
        document = f.read()
        f.close()
        terms = tokenize(document)
        num_c4+=len(terms)#类4总词数
        unique_terms = set(terms)
        for term in unique_terms:
            if term not in postings4:
                postings4[term] = (terms.count(term))
            else:
                postings4[term] =(postings4[term]+(terms.count(term)))
    
   
    for id in doc5_filenames:
        f = open(doc5_filenames[id],'r',encoding='utf-8',errors='ignore')
        document = f.read()
        f.close()
        terms = tokenize(document)
        num_c5+=len(terms)#类5总词数    
        unique_terms = set(terms)
        for term in unique_terms:
            if term not in postings5:
                postings5[term] = (terms.count(term))
            else:
                postings5[term] =(postings5[term]+(terms.count(term)))
                
def tokenize(document):
    
    document=document.lower()
    document=re.sub(r"\W|\d|_|\s{2,}"," ",document)
    terms=TextBlob(document).words.singularize()

    result=[]
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")
        result.append(expected_str)
    return result 


def getClass_dic():
    #小规模测试文档路径
    global doc1_filenames,doc2_filenames,doc3_filenames,doc4_filenames,doc5_filenames
    Newspath1=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_train\alt.atheism")
    Newspath2=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_train\comp.graphics")
    Newspath3=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_train\rec.sport.hockey")
    Newspath4=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_train\comp.sys.ibm.pc.hardware")
    Newspath5=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework2NBC\20news-18828_train\comp.sys.mac.hardware")

    files=[f for f in  os.listdir(Newspath1)]
    i=0
    for fi in files:       
        doc1_filenames.update({i:os.path.join(Newspath1,fi)})
        i+=1

    files=[f for f in  os.listdir(Newspath2)]
    i=0
    for fi in files:       
        doc2_filenames.update({i:os.path.join(Newspath2,fi)})
        i+=1

    files=[f for f in  os.listdir(Newspath3)]
    i=0
    for fi in files:       
        doc3_filenames.update({i:os.path.join(Newspath3,fi)})
        i+=1

    files=[f for f in  os.listdir(Newspath4)]
    i=0
    for fi in files:       
        doc4_filenames.update({i:os.path.join(Newspath4,fi)})
        i+=1

    files=[f for f in  os.listdir(Newspath5)]
    i=0
    for fi in files:       
        doc5_filenames.update({i:os.path.join(Newspath5,fi)})
        i+=1
    
    
def test(Newspath1,ss):
    global total_aRate
    nc1=len(postings1)
    nc2=len(postings2)
    nc3=len(postings3)
    nc4=len(postings4)
    nc5=len(postings5)
    
    doc1_test={}
    files=[f for f in  os.listdir(Newspath1)]
    i=0
    for fi in files:       
        doc1_test.update({i:os.path.join(Newspath1,fi)})
        i+=1
    
    count1=0
    
    for id in doc1_test:
        f = open(doc1_test[id],'r',encoding='utf-8',errors='ignore')
        document = f.read()
        f.close()
        terms = tokenize(document)
        p=[0,0,0,0,0]
        for term in terms:
            if term in postings1:
                p[0]+=math.log((postings1[term]+1)/(num_c1+nc1))
            else:
                p[0]+=math.log(1/(num_c1+nc1))
                
            if term in postings2:
                p[1]+=math.log((postings2[term]+1)/(num_c2+nc2))
            else:
                p[1]+=math.log(1/(num_c2+nc2))
                
            if term in postings3:
                p[2]+=math.log((postings3[term]+1)/(num_c3+nc3))
            else:
                p[2]+=math.log(1/(num_c3+nc3))
                
            if term in postings4:
                p[3]+=math.log((postings4[term]+1)/(num_c4+nc4))
            else:
                p[3]+=math.log(1/(num_c4+nc4))
            if term in postings5:
                p[4]+=math.log((postings5[term]+1)/(num_c5+nc5))
            else:
                p[4]+=math.log(1/(num_c5+nc5))
        
        if p[ss]==max(p):
            count1+=1
    print(ss+1,"类名：",Newspath1[74:])
    print("判对文档数：",count1,"总的文档数：",len(doc1_test))
    total_aRate = (total_aRate+count1/len(doc1_test))
    print("准确率为：",count1/len(doc1_test))
    
    
if __name__ == "__main__":
    main()

