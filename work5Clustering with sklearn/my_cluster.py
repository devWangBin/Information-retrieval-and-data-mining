# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:42:15 2018

@author: 93568
"""
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.cluster import KMeans
from collections import defaultdict
from textblob import TextBlob
from textblob import Word
from sklearn.externals import joblib


ground_truth = []                   #每条推特的正确聚类标签
tweets_list = []                    #处理过的推特内容列表
tweet_num = 0                       #推特总数目

def main():
    tweets_process()
    print("ground_truth 数目:",len(ground_truth))
    print("gt 标签最小值:",min(ground_truth))
    print("gt 标签最大值:",max(ground_truth))
    print("number of tweets:",tweet_num)
    result = Kmeans_cluter()
    
    for t in range(len(result)):
        result[t]+=1
        
    
    print("result 最小值:",min(result))
    print("result 最大值:",max(result))
    if len(result)==tweet_num:
        crrect_num = 0
        for i in range(0,tweet_num-1):
            if result[i] == ground_truth[i]:
                crrect_num+=1
    print("crrect number is:",crrect_num)


def token(line):
    
    index = line.index(",")
    Text = line[10:index-1]
    cluNumber = line[index+12:-2]
    return (Text,cluNumber)


def tweets_process():
    global ground_truth,tweets_list,tweet_num
    print("tweets processing...")
    f = open(r"C:\Users\93568\Documents\GitHub\DataMining\work5Clustering with sklearn\data\Homework5Tweets.txt")  
    lines = f.readlines()#读取全部内容
    
    count = 0
    for line in lines:
        
        (text,cluNumber) = token(line)      
        number = int(cluNumber)
        tweets_list.append(text)
        ground_truth.append(number)
        count+=1    
    tweet_num = count



def token_split(text):
    #doc = doc.lower()
    terms=TextBlob(text).words.singularize()
    
    result=[]
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")     
        result.append(expected_str)
    
    return result    
 
  
def Kmeans_cluter():

    tfidf_vectorizer = TfidfVectorizer(tokenizer=token_split, lowercase=True)
    '''
    tokenizer: 指定分词函数
    lowercase: 在分词之前将所有的文本转换成小写，因为涉及到中文文本处理，
    所以最好是False
    '''
    
    #tfidf_matrix = tfidf_vectorizer.fit_transform(tweets_list)
    #上面一行代码等价于下面两行代码
    tfidf_vectorizer.fit(tweets_list)
    tfidf_matrix = tfidf_vectorizer.transform(tweets_list)
    
 
    num_clusters = max(ground_truth)  #与原本标签类别数目保持一致，其实并不合理
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=500, n_init=30, \
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
    #result = km_cluster.fit_predict(tfidf_matrix)
    #上面一行代码等价于下面两行代码
    km_cluster.fit(tfidf_matrix)
    result = km_cluster.predict(tfidf_matrix)
    
    joblib.dump(tfidf_matrix, 'tfidf_matrix.pkl')
    joblib.dump(tfidf_vectorizer, 'tfidf_fit_result.pkl')
    joblib.dump(km_cluster, 'km_cluster_fit_result.pkl')
 
    #程序下一次则可以直接load
#    tfidf_vectorizer = joblib.load('tfidf_fit_result.pkl')
#    km_cluster = joblib.load('km_cluster_fit_result.pkl')
     
    print ("Predicting result length: ", len(result))
    
    return result           




if __name__ == "__main__":
    main()