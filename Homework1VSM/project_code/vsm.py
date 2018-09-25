from collections import defaultdict
from functools import reduce  
import math
import sys
import os
import re

# 测试文档路径
#Newspath=(r"C:\Users\93568\Documents\GitHub\DataMining\Homework1VSM\20news-18828")
Newspath=(r"C:\Users\93568\Documents\GitHub\0123")
folders=[f for f in  os.listdir(Newspath)]
print(folders)

files=[]
for folderName in  folders:
    folderPath=os.path.join(Newspath, folderName)
    files.append([f for f in os.listdir(folderPath)])

#print(sum(len(files[i])for i in range(20)))
document_filenames={}
i=0
for fo in range(len(folders)):
    for fi in files[fo] :
        #document_filenames[i].append(os.path.join(Newspath, os.path.join(folders[fo],fi)))
        document_filenames.update({i:os.path.join(Newspath,os.path.join(folders[fo],fi))})
        i+=1


N = len(document_filenames)

# 词典
dictionary = set()

# postings[term][id] 表示在文档 id 内term词的词频
postings = defaultdict(dict)

document_frequency = defaultdict(int)

# 文档总数
length = defaultdict(float)

# 用于tokenize的字符
characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>+/|_"

def main():
    initialize_terms_and_postings()
    initialize_document_frequencies()
    #initialize_lengths()
    p_dictionary()
    #while True:
        #do_search()

def p_dictionary():
    i = 0
    fp=open(r"C:\Users\93568\Documents\GitHub\dictest.txt",'w',encoding='utf-8')
    fp.write("<<VAM_DICTIONARY>>"+'\n')
    for term in dictionary:
        fp.write(term+' ')
        i+=1
        #fp.write(' ')
        if i%200==0:
            fp.write('\n')
    fp.close()

def initialize_terms_and_postings():
   
    global dictionary, postings
    for id in document_filenames:
        f = open(document_filenames[id],'r',encoding='utf-8',errors='ignore')
        document = f.read()
        f.close()
        terms = tokenize(document)
        unique_terms = set(terms)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
            postings[term][id] = terms.count(term) # the value is the
                                                   # frequency of the
                                                   # term in the
                                                   # document

def tokenize(document):
    terms=document.lower()
    terms=terms.replace("\n"," ")
    terms=terms.replace("\t"," ")
    terms=terms.replace(","," ")
    terms=terms.replace(":"," ")
    terms=terms.replace("."," ")
    terms=terms.replace("("," ")
    terms=terms.replace(")"," ")
    terms=terms.replace("\\"," ")
    terms=terms.replace("/"," ")
    terms=terms.replace("\""," ")
    terms=terms.replace("-"," ")
    terms=terms.replace("~"," ")
    terms=terms.replace("?"," ")
    terms=re.sub(r"\s{2,}"," ",terms)
    terms=terms.split()
    return [term.strip(characters) for term in terms]

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
