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
    answer = []
    
    if (term1 not in postings) or (term2 not in postings):
        return answer      
    else:
        i = len(postings[term1])
        j = len(postings[term2])
        x=0
        y=0
        while x<i and y<j:
            if postings[term1][x]==postings[term2][y]:
                answer.append(postings[term1][x])
                x+=1
                y+=1
            elif postings[term1][x] < postings[term2][y]:
                x+=1
            else:
                y+=1            
        return answer                        

def merge2_or(term1,term2):
    answer=[]
    if (term1 not in postings)and(term2 not in postings):
        answer = []      
    elif term2 not in postings:
        answer = postings[term1]
    elif term1 not in postings:
         answer = postings[term2]
    else:
        answer = postings[term1]
        for item in postings[term2]:
            if item not in answer:
                answer.append(item)              
    return answer

def merge2_not(term1,term2):
    answer=[]
    if term1 not in postings:
        answer.append("not find!")       
    elif term2 not in postings:
        answer = postings[term1]
        
    else:
        answer = postings[term1]
        i = len(answer)
        j = len(postings[term2])
        x=0
        y=0
        while x<i and y<j:
            if answer[x]==postings[term2][y]:                
                y+=1
                answer.pop(x)
            elif answer[x] < postings[term2][y]:
                x+=1
            else:
                y+=1
                
    return answer

def merge3_and(term1,term2,term3):
    Answer = []
    if term3 not in postings:
        return Answer   
    else:
        Answer = merge2_and(term1,term2)
        if Answer==[]:
            return Answer
        ans = []
        i = len(Answer)
        j = len(postings[term3])
        x=0
        y=0
        while x<i and y<j:
            if Answer[x]==postings[term3][y]:
                ans.append(Answer[x])
                x+=1
                y+=1
            elif Answer[x] < postings[term3][y]:
                x+=1
            else:
                y+=1
        
        return ans

def merge3_or(term1,term2,term3):
    Answer = []
    Answer = merge2_or(term1,term2);
    if term3 not in postings:
        return Answer
    else:
        if Answer ==[]:
            Answer = postings[term3]
        else:
            for item in postings[term3]:
                if item not in Answer:
                    Answer.append(item)
        return Answer

def merge3_and_or(term1,term2,term3):
    Answer = []
    Answer = merge2_and(term1,term2)
    if term3 not in postings:
        return Answer
    else:
        if Answer==[]:
            Answer = postings[term3]
            return Answer
        else:
            for item in postings[term3]:
                if item not in Answer:
                    Answer.append(item)
            return Answer

def merge3_or_and(term1,term2,term3):
    Answer = []
    Answer = merge2_or(term1,term2)
    if (term3 not in postings) or (Answer==[]):
        return Answer
    else:
        ans = []
        i = len(Answer)
        j = len(postings[term3])
        x=0
        y=0
        while x<i and y<j:
            if Answer[x]==postings[term3][y]:
                ans.append(Answer[x])
                x+=1
                y+=1
            elif Answer[x] < postings[term3][y]:
                x+=1
            else:
                y+=1       
        return ans       

def do_rankSearch(terms):
    Answer = defaultdict(dict)
    for item in terms:
        if item in postings:
            for tweetid in postings[item]:
                if tweetid in Answer:
                    Answer[tweetid]+=1
                else:
                    Answer[tweetid] = 1
    Answer = sorted(Answer.items(),key = lambda asd:asd[1],reverse=True)
    return Answer


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
       line.pop(0);
       unique_terms = set(line)
       for te in unique_terms:
           if te in postings.keys():                         
               postings[te].append(tweetid)           
           else:            
               postings[te] = [tweetid]
    #按字典序对postings进行升序排序,但返回的是列表，失去了键值的信息
    #postings = sorted(postings.items(),key = lambda asd:asd[0],reverse=False)       
    print(len(postings))
    
    
    
def do_search():
    terms = token(input("Search query >> "))
    if terms == []:
        sys.exit()  
    #搜索的结果答案   
    
    if len(terms)==3:
        #A and B
        if terms[1]=="and":
            answer = merge2_and(terms[0],terms[2])          
        #A or B       
        elif terms[1]=="or":
            answer = merge2_or(terms[0],terms[2])           
        #A not B    
        elif terms[1]=="not":
            answer = merge2_not(terms[0],terms[2])
        #输入的三个词格式不对    
        else:
            print("input wrong!")
        
    elif len(terms)==5:
        #A and B and C
        if (terms[1]=="and") and (terms[3]=="and"):
            answer = merge3_and(terms[0],terms[2],terms[4])
            print(answer)
        #A or B or C
        elif (terms[1]=="or") and (terms[3]=="or"):
            answer = merge3_or(terms[0],terms[2],terms[4])
            print(answer)
        #(A and B) or C
        elif (terms[1]=="and") and (terms[3]=="or"):
            answer = merge3_and_or(terms[0],terms[2],terms[4])
            print(answer)
        elif (terms[1]=="or") and (terms[3]=="and"):
            answer = merge3_or_and(terms[0],terms[2],terms[4])
            print(answer)
        else:
            print("More format is not supported now!")
    #进行自然语言的排序查询，返回按相似度排序的最靠前的若干个结果
    else:
        leng = len(terms)
        answer = do_rankSearch(terms)
        print ("[Rank_Score: Tweetid]")
        for (tweetid,score) in answer:
            print (str(score/leng)+": "+tweetid)

def main():
    get_postings()
    while True:
        do_search()


if __name__ == "__main__":
    main()
