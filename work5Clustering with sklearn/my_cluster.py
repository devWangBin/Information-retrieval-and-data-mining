# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:42:15 2018

@author: 93568
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster
from collections import defaultdict
from textblob import TextBlob
from textblob import Word
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.externals import joblib#用于存储文件

label_tweetid = {}                  #  {cluster标号[tweetid01,tweetid02...]...},有些多余...
ground_truth = []                   #每条推特的正确聚类标签  [37,5,8,58......]
tweets_list = []                    #处理过的推特内容列表  [推特内容1，内容2，......]
tweet_num = 0                       #推特总数目
class_num = 0                       #类别数目
tfidf_matrix = []
tfidf_matrix = joblib.load('tfidf_matrix.pkl')


def main():
    global label_tweetid,class_num,ground_truth    
    
    tweets_process()
    
    class_num = len(label_tweetid)
    print("number of tweets:",tweet_num)
    print("number of labels:",class_num)
#    使用sort会出错
#    label_Tweetid = sorted(label_tweetid.keys(), key=lambda asd:asd[0], reverse = False)
#    应该使用以下方法排序规范化处理
#    label_tweetid = label_progress(label_tweetid)#将原本的{cluster类别号[tweetid01,tweetid02...]...}对类别好进行排序处理
#    print(label_tweetid)
    
    result = Kmeans_cluster()
    NMI_score_Kmeans = normalized_mutual_info_score(ground_truth,result)
    
    result = AffinityPropagation_cluster()
    NMI_score_af = normalized_mutual_info_score(ground_truth,result)
    
    result = meanshift_cluster()
    NMI_score_meanshift = normalized_mutual_info_score(ground_truth,result)
    
    result = DBSCN_cluster()
    NMI_score_DBSCN = normalized_mutual_info_score(ground_truth,result)
    
    result = S_C_cluster()
    NMI_score_SpectralClustering = normalized_mutual_info_score(ground_truth,result)
    
    result = AgglomerativeClustering_cluster()
    NMI_score_Agg = normalized_mutual_info_score(ground_truth,result)
#    See also其它聚类评价方法
#    v_measure_score()
#       V-Measure (NMI with arithmetic mean option.)
#    adjusted_rand_score()
#       Adjusted Rand Index
#    adjusted_mutual_info_score()
#       Adjusted Mutual Information (adjusted against chance)
    
    print("NMI_score_Kmeans:\t",NMI_score_Kmeans)
    print("NMI_score_af:\t",NMI_score_af)
    print("NMI_score_meanshift:\t",NMI_score_meanshift)
    print("NMI_score_DBSCN:\t",NMI_score_DBSCN)
    print("NMI_score_SpectralClustering:\t",NMI_score_SpectralClustering)
    print("NMI_score_Agg:\t",NMI_score_Agg)
    
#    以下是自己编写的聚类结果评价方法，效果不行放弃！    
#    new_result = result_process(result)
#    print(len(new_result))      
#    crrect_num = 0
#    for key in range(1,label_num):
#        intersection = list(set(label_tweetid[key]).intersection(set(new_result[key])))
#        crrect_num += len(intersection)
#    print("crrect number is:",crrect_num)

def label_progress(label_tweetid):
    new_label_tweetid = {}
    i = 1
    for key in label_tweetid.keys():
        new_label_tweetid[i] = label_tweetid[key]
        i+=1
    
    return new_label_tweetid

def result_process(result):     #对传入的result聚类结果result[1,2,3.......]
                                #预测标签的列表进行处理得到字典{cluster类别号[tweetid01,tweetid02...]...}
    global label_tweetid
    newResult = {}
    
    for label in range(0,len(label_tweetid)):
        for item in range(0,len(result)):
            if result[item]==label:
                if label not in newResult.keys():               
                    newResult[label] = []
                    newResult[label].append(item+1)
                else:
                    newResult[label].append(item+1)
    
    return newResult


def token(line):
    
    index = line.index(",")
    Text = line[10:index-1]
    cluNumber = line[index+12:-2]
    return (Text,cluNumber)


def tweets_process():
    global ground_truth,tweets_list,tweet_num,label_tweetid
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
        if number not in label_tweetid:
            label_tweetid[number] = []
            label_tweetid[number].append(count)
        else:
            label_tweetid[number].append(count)
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


def AffinityPropagation_cluster():
    
    global tfidf_matrix    
    af = AffinityPropagation(preference=-50).fit(tfidf_matrix)
    return af.labels_
    
def meanshift_cluster():
    
    global tfidf_matrix    
    clustering = MeanShift(bandwidth=2).fit(tfidf_matrix)
    return clustering.labels_
    
def DBSCN_cluster():
    global tfidf_matrix
    db = DBSCAN(eps=0.3, min_samples=10).fit(tfidf_matrix)
    return db.labels_

def S_C_cluster():
    
    global tfidf_matrix
    clustering = SpectralClustering(n_clusters=2,
                                    assign_labels="discretize",
                                    random_state=0).fit(tfidf_matrix)
    return clustering.labels_

def AgglomerativeClustering_cluster():
    global tfidf_matrix
    clustering = AgglomerativeClustering().fit(tfidf_matrix)
    return clustering.labels_

def FeatureAgglomeration_cluster():
     global tfidf_matrix
     agglo = cluster.FeatureAgglomeration(n_clusters=32)
     agglo.fit(tfidf_matrix)     
     return agglo.labels_

def MiniBatchKMeans_cluter():
    
    kmeans = MiniBatchKMeans(n_clusters=2,
                             random_state=0,
                             batch_size=6,
                             max_iter=10).fit(X)

 
def Kmeans_cluster():

#    tfidf_vectorizer = TfidfVectorizer(tokenizer=token_split, lowercase=True)
#    '''
#    tokenizer: 指定分词函数
#    lowercase: 在分词之前将所有的文本转换成小写，因为涉及到中文文本处理，
#    所以最好是False
#    '''    
#    #tfidf_matrix = tfidf_vectorizer.fit_transform(tweets_list)
#    #上面一行代码等价于下面两行代码
#    tfidf_vectorizer.fit(tweets_list)
#    tfidf_matrix = tfidf_vectorizer.transform(tweets_list)
    tfidf_matrix = []
    tfidf_matrix = joblib.load('tfidf_matrix.pkl')
    print("tfidf矩阵维度:",tfidf_matrix.shape)    
    num_clusters = len(label_tweetid)  #与原本标签类别数目保持一致，其实并不合理
        
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=100, n_init=10, \
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
    Result = km_cluster.labels_

#    对于新数据的预测    
#    result = km_cluster.predict(tfidf_matrix)
    
#    joblib.dump(tfidf_matrix, 'tfidf_matrix.pkl')
#    程序下一次则可以直接load
#    tfidf_vectorizer = joblib.load('tfidf_fit_result.pkl')
    
    print ("Predicting result length: ", len(Result))   
    return Result           


if __name__ == "__main__":
    main()