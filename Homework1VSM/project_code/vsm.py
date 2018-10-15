from textblob import TextBlob
from textblob import Word
from collections import defaultdict
from functools import reduce  
import math
import sys
import os
import re

# 测试文档路径
#Newspath=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework1VSM\20news-18828")

#小规模测试文档路径
Newspath=(r"C:\Users\93568\Documents\GitHub\0123")

folders=[f for f in  os.listdir(Newspath)]
print(folders)

files=[]
for folderName in  folders:
    folderPath=os.path.join(Newspath, folderName)
    files.append([f for f in os.listdir(folderPath)])

document_filenames={}
i=0

for fo in range(len(folders)):
    for fi in files[fo]:       
        document_filenames.update({i:os.path.join(Newspath,os.path.join(folders[fo],fi))})
        i+=1
#文档总数
N = len(document_filenames)
# 词典
dictionary = set()
# postings[term][id] 表示在文档 id 内term词的词频
postings = defaultdict(dict)
#文档词频
document_frequency = defaultdict(int)
# 文档重要性集合，用于查询计算相似性
length = defaultdict(float)
# 用于tokenize的字符
#characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>+/|_"
def main():
    initialize_terms_and_postings()
    initialize_document_frequencies()
    initialize_lengths()
    p_dictionary()
    while True:
        do_search()

def p_dictionary():
    i = 0
    fp=open(r"C:\Users\93568\Documents\GitHub\dic.txt",'w',encoding='utf-8') 
    fp.write("<<VAM_DICTIONARY>>"+'\n')
    for term in dictionary:
        fp.write(term+' ')
        i+=1
        if i%200==0:
            fp.write('\n')
    fp.close()
    print(postings)
    #print(postings)

def initialize_terms_and_postings():
    global dictionary, postings
    for id in document_filenames:
        f = open(document_filenames[id],'r',encoding='utf-8',errors='ignore')
        document = f.read()
        f.close()
        terms = tokenize(document)
        d_tnum=len(terms)#预处理后每篇文档的总词数
        #print(d_tnum)
        unique_terms = set(terms)
        dictionary = dictionary.union(unique_terms)#并入总词典
        for term in unique_terms:
            c_term=terms.count(term)
            
            #postings[term][id] = (terms.count(term))/d_tnum
            if c_term>0:
                postings[term][id]=1+math.log(c_term)
            else:
                postings[term][id]=0
            # the value is the frequency of term in the document
def tokenize(document):
    
    document=document.lower()
    #document=re.sub(r'', " ",document)
    document=re.sub(r"\W|\d|_|\s{2,}"," ",document)
    terms=TextBlob(document).words.singularize()
    
    result=[]
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")
        result.append(expected_str)
    return result 
    

def initialize_document_frequencies():
    global document_frequency
    for term in dictionary:
        document_frequency[term] = len(postings[term])

def initialize_lengths():
    global length
    for id in document_filenames:
        l = 0
        for term in dictionary:
            l += imp(term,id)**2
        length[id] = math.sqrt(l)

def imp(term,id):
   
    if id in postings[term]:
        return postings[term][id]*inverse_document_frequency(term)
    else:
        return 0.0

def inverse_document_frequency(term):
    
    if term in dictionary:
        return math.log(N/document_frequency[term],2)
    else:
        return 0.0

def do_search():
       
    query = tokenize(input("Search query >> "))
    if query == []:
        sys.exit()
    # find document ids containing all query terms.  Works by
    # intersecting the posting lists for all query terms.
    relevant_document_ids = intersection(
            [set(postings[term].keys()) for term in query])
    if not relevant_document_ids:
        print ("No documents matched all query terms.")
    else:
        scores = sorted([(id,similarity(query,id))
                         for id in relevant_document_ids],
                        key=lambda x: x[1],
                        reverse=True)
        print ("Score: filename")
        for (id,score) in scores:
            print (str(score)+": "+document_filenames[id])

def intersection(sets):
   
    return reduce(set.intersection, [s for s in sets])

def similarity(query,id):
   
    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*imp(term,id)
    similarity = similarity / length[id]
    return similarity

if __name__ == "__main__":
    main()
