# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 09:50:40 2018

@author: 93568
"""
import numpy as np
import matplotlib.pyplot as plt
import jieba 
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.cluster import KMeans

 
def jieba_tokenize(text):
    return jieba.lcut(text) 
 
 
tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, \
                                   lowercase=True)


'''
tokenizer: 指定分词函数
lowercase: 在分词之前将所有的文本转换成小写，因为涉及到中文文本处理，
所以最好是False
'''
text_list = ["今天天气真好啊啊啊啊", "小明上了清华大学", \
"我今天拿到了Google的Offer", "清华大学在自然语言处理方面真厉害"]
 #需要进行聚类的文本集
 
tfidf_matrix = tfidf_vectorizer.fit_transform(text_list)
#上面一行代码等价于下面两行代码
#tfidf_vectorizer.fit(text_list)
#tfidf_matrix = tfidf_vectorizer.transform(text_list)
print(tfidf_vectorizer)
print(tfidf_matrix)
 
num_clusters = 3
km_cluster = KMeans(n_clusters=num_clusters, max_iter=30, n_init=4, \
                    init='k-means++',n_jobs=1)
'''
n_clusters: 指定K的值
max_iter: 对于单次初始值计算的最大迭代次数
n_init: 重新选择初始值的次数
init: 制定初始值选择的算法
n_jobs: 进程个数，为-1的时候是指默认跑满CPU
注意，这个对于单个初始值的计算始终只会使用单进程计算，
并行计算只是针对与不同初始值的计算。比如n_init=10，n_jobs=40, 
服务器上面有20个CPU可以开40个进程，最终只会开10个进程
'''
#返回各自文本的所被分配到的类索引
result = km_cluster.fit_predict(tfidf_matrix)
#上面一行代码等价于下面两行代码
#km_cluster.fit(tfidf_matrix)
#result = km_cluster.predict(tfidf_matrix)
 
print ("Predicting result: ", result)















