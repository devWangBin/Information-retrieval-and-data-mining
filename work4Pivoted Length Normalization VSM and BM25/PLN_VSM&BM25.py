# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 21:44:33 2018

@author: 93568
"""

import sys
import math
from functools import reduce  # py3
from textblob import TextBlob
from textblob import Word
from collections import defaultdict

uselessTerm = ["username","text","tweetid"]
postings = defaultdict(dict)
document_frequency = defaultdict(int)
document_lengths= defaultdict(int)
document_numbers = len(document_lengths)
avdl=0

def main():
    get_postings_dl()
    initialize_document_frequencies()
    initialize_avdl()
    #print(postings)
    #print(document_lengths) 
    
    print("平均tweet 长度为："+str(avdl))
    #可以修改do_search方法中的返回数据，得到使用不同模型的result
    #my_result_PLN.txt/my_result_BM25.txt/
    result_name = "my_result_PLN_BM25.txt"
    
    get_result(result_name)
    
    
    

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
    global uselessTerm
    document=document.lower()
    a = document.index("username")
    b = document.index("clusterno")
    c = document.rindex("tweetid")-1
    d = document.rindex("errorcode")
    e = document.index("text")
    f = document.index("timestr")-3  
    #提取用户名、tweet内容和tweetid三部分主要信息
    document = document[c:d]+document[a:b]+document[e:f]
    terms=TextBlob(document).words.singularize()
      
    result=[]
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")
        if expected_str not in uselessTerm:
            result.append(expected_str)

    return result

def get_queries():
    #输入为qrels2014.txt
    #输出为对于查询token后的结果:id + 查询字符串
    queries = {}
    keyid = 171
    
    fq = open(r"C:\Users\93568\Documents\GitHub\DataMining\work4Pivoted Length Normalization VSM and BM25\data\qrels2014.txt")
    lines = fq.readlines()
    
    for line in lines:
        
        index1 = line.find("<query>")
        
        if index1>=0:
            #得到<query>和</query>之间的查询内容
            index1 += 8
            index2 = line.find("</query>")
            #print(line[index1:index2])
            
            #添加到queries字典
            queries[keyid] = line[index1:index2]
            keyid+=1
    
    return queries


def get_postings_dl():
    
    global postings,document_lengths
    f = open(r"C:\Users\93568\Documents\GitHub\DataMining\work4Pivoted Length Normalization VSM and BM25\data\tweets.txt")  
    lines = f.readlines()#读取全部内容

    for line in lines:
       line = tokenize_tweet(line)
       tweetid = line[0]
       line.pop(0)
       document_lengths[tweetid] = len(line)
       unique_terms = set(line)
       for te in unique_terms:
          postings[te][tweetid] = line.count(te)
    #按字典序对postings进行升序排序,但返回的是列表，失去了键值的信息
    #postings = sorted(postings.items(),key = lambda asd:asd[0],reverse=False)       
    #print(postings)
    
def initialize_document_frequencies():
   
    global document_frequency,postings
    for term in postings:
        document_frequency[term] = len(postings[term])

def initialize_avdl():
    global document_lengths,avdl
    count = 0
    for twid in document_lengths:
        count += document_lengths[twid]
    avdl = count/len(document_lengths)



def get_result(file_name):
    
    with open(file_name, 'w', encoding='utf-8') as f_out:
       
        Quaries = get_queries()        
        qkeys = Quaries.keys()
        
        for key in qkeys:
            
            q_result = do_search(Quaries[key])
            
            for tweetid in q_result:
                
                f_out.write(str(key)+' '+tweetid+'\n')
    


def do_search(query):
    
    result = []#返回对于query的所有tweetid排序后的列表
    
    query = token(query)
    
    if query == []:
        sys.exit()
    
    unique_query = set(query)
    #避免遍历所有的tweet，可先提取出有相关性的tweetid，tweet中包含查询的关键词之一便可认为相关
    relevant_tweetids = Union([set(postings[term].keys()) for term in unique_query])
    
    #print(relevant_tweetids)
    
    if not relevant_tweetids:
        print ("No tweets matched any query terms for")
        print(query)
    else:
        #PLN
#        scores1 = sorted([(id,similarity_PLN(query,id))
#                         for id in relevant_tweetids],
#                        key=lambda x: x[1],
#                        reverse=False)
        #BM25
#        scores2 = sorted([(id,similarity_BM25(query,id))
#                         for id in relevant_tweetids],
#                        key=lambda x: x[1],
#                        reverse=False)
        
        #PLN+BM25
        scores3 = sorted([(id,similarity_BM25(query,id)+similarity_PLN(query,id))
                         for id in relevant_tweetids],
                        key=lambda x: x[1],
                        reverse=False)
      
        for (id,score) in scores3:

            result.append(id)
    
    return result
#    print ("<<<<<Score(PLN)--Tweeetid>>>>>")
#    print("PLN一共有"+str(len(scores1))+"条相关tweet！")
#    for (id,score) in scores1:
#        print (str(score)+": "+id)
#        
#    print ("<<<<<Score(BM25)--Tweeetid>>>>>")
#    print("BM25一共有"+str(len(scores2))+"条相关tweet！")
#    for (id,score) in scores2:
#        print (str(score)+": "+id)

def similarity_PLN(query,id):
    global postings,avdl
    fenmu =1 - 0.1 + 0.1*(document_lengths[id]/avdl)
    similarity = 0.0
    unique_query = set(query)
    for term in unique_query:
        if (term in postings) and (id in postings[term].keys()):
            #使用ln(1+ln(C(w,d)+1))后发现相关性的分数都为负数很小
            similarity += ((query.count(term))*(math.log(math.log(postings[term][id] + 1) + 1))*math.log((document_numbers+1)/document_frequency[term]))/fenmu            
        
    return similarity

def similarity_BM25(query,id):
    global postings,avdl
    fenmu =1 - 0.2 + 0.2*(document_lengths[id]/avdl)
    k = 1
    similarity = 0.00
    
    unique_query = set(query)
    for term in unique_query:
        if (term in postings) and (id in postings[term].keys()):
            C_wd = postings[term][id]
            #使用ln(1+ln(C(w,d)+1))后发现相关性的分数都为负数很小
            similarity += (query.count(term)*(k+1)*C_wd*math.log((document_numbers+1)/document_frequency[term]))/(k*fenmu+C_wd)            
            
    return similarity


def Union(sets):    
    return reduce(set.union, [s for s in sets])

if __name__ == "__main__":
    main()
    