# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 17:49:54 2018

@author: 93568
"""
#调用sklearn的各种聚类算法对tweet数据集进行聚类
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.cluster import SpectralClustering
from sklearn.mixture import GaussianMixture
from textblob import TextBlob
from textblob import Word
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.externals import joblib#用于存储文件

tfidf_matrix = []                   #全局变量tf_idf矩阵(2472, 4640)
ground_truth = []                   #每条推特的正确聚类标签  [37,5,8,58......]
tweets_list = []                    #处理过的推特内容列表  [推特内容1，内容2，......]

def main():
    global ground_truth,tfidf_matrix
    
    tweets_process()
    
    
    #得到实际标签类别数目
    setLabel = set(ground_truth)
    label_num = len(setLabel)
    print("number of class labels:",label_num)
    #加载tfidf矩阵
    #get_tfidf_matrix()
    tfidf_matrix = joblib.load('tfidf_matrix.pkl')
    print(tfidf_matrix.shape)
    #矩阵稀疏
    tfidf_matrix = tfidf_matrix*10
    tfidf_matrix = tfidf_matrix.toarray()
    
    #KMeans  
    km_cluster = KMeans(n_clusters=label_num, max_iter=200, n_init=20, \
                        init='k-means++',n_jobs=1)
    km_cluster.fit(tfidf_matrix)
    result = km_cluster.labels_
    NMI_score_Kmeans = normalized_mutual_info_score(ground_truth,result)
    
    #AffinityPropagation
    af = AffinityPropagation().fit(tfidf_matrix)
    result = af.labels_
    NMI_score_af = normalized_mutual_info_score(ground_truth,result)
    
    #MeanShift    
    bandwidth = estimate_bandwidth(tfidf_matrix, quantile=0.2, n_samples=500)    
    clustering = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(tfidf_matrix)
    result = clustering.labels_
    NMI_score_meanshift = normalized_mutual_info_score(ground_truth,result)
    
    #DBSCN
    db = DBSCAN().fit(tfidf_matrix)
    result = db.labels_
    NMI_score_DBSCN = normalized_mutual_info_score(ground_truth,result)   

    #SpectralClustering
    clustering = SpectralClustering(n_clusters=2,
                                    assign_labels="discretize",
                                    random_state=0).fit(tfidf_matrix)
    result = clustering.labels_
    NMI_score_SpectralClustering = normalized_mutual_info_score(ground_truth,result)
    
    #AgglomerativeClustering
    clustering = AgglomerativeClustering().fit(tfidf_matrix)
    result = clustering.labels_
    NMI_score_Agg = normalized_mutual_info_score(ground_truth,result)
    
    #ward hierarchical clustering
    ward = AgglomerativeClustering(n_clusters=label_num, linkage='ward')
    ward.fit(tfidf_matrix)
    result = ward.labels_
    NMI_score_Ward_hc = normalized_mutual_info_score(ground_truth,result)
    
    #Birch
    brc = Birch(branching_factor=50, n_clusters=None, threshold=0.5,compute_labels=True)
    brc.fit(tfidf_matrix) 
    result = brc.labels_
    NMI_score_Brich = normalized_mutual_info_score(ground_truth,result)
    
#    #Gaussian mixtures    
#    Gaussian_mixtures = GaussianMixture(n_components=label_num, covariance_type='full', init_params='kmeans')
#    #for covar_type in ['spherical', 'diag', 'tied', 'full']
#    Gaussian_mixtures.fit(tfidf_matrix)     
#    result = Gaussian_mixtures.labels_
#    NMI_score_Gaussian_m = normalized_mutual_info_score(ground_truth,result)
    
#    See also其它聚类评价方法
#    v_measure_score()
#       V-Measure (NMI with arithmetic mean option.)
#    adjusted_rand_score()
#       Adjusted Rand Index
#    adjusted_mutual_info_score()
#       Adjusted Mutual Information (adjusted against chance)
    
    print("NMI_score_Kmeans:\t",NMI_score_Kmeans)
    print("NMI_score_AffP:\t",NMI_score_af)
    print("NMI_score_meanshift:\t",NMI_score_meanshift)
    print("NMI_score_SpectralClustering:\t",NMI_score_SpectralClustering)
    print("NMI_score_Ward_hc:\t\t",NMI_score_Ward_hc)
    print("NMI_score_Agg:\t\t\t",NMI_score_Agg)    
    print("NMI_score_DBSCN:\t",NMI_score_DBSCN)
#    print("NMI_score_Gaussian_mixtures:\t",NMI_score_Gaussian_m)
    print("NMI_score_Birch:\t\t",NMI_score_Brich)
    
    print("All cluster methods have been done!Great!!!")


def token(line):    
    index = line.index(",")
    Text = line[10:index-1]
    cluNumber = line[index+12:-2]
    return (Text,cluNumber)


def tweets_process():
    global ground_truth,tweets_list
    print("tweets processing...")
    f = open(r"C:\Users\93568\Documents\GitHub\DataMining\work5Clustering with sklearn\data\Homework5Tweets.txt")  
    lines = f.readlines()#读取全部内容    
    for line in lines:       
        (text,cluNumber) = token(line)      
        number = int(cluNumber)
        tweets_list.append(text)
        ground_truth.append(number)


def token_split(text):
    #doc = doc.lower()
    terms=TextBlob(text).words.singularize()   
    result=[]
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")     
        result.append(expected_str)    
    return result    

def get_tfidf_matrix():
    global tfidf_matrix,tweets_list
    tfidf_vectorizer = TfidfVectorizer(tokenizer=token_split, lowercase=True)
    '''
    tokenizer: 指定分词函数
    lowercase: 在分词之前将所有的文本转换成小写，因为涉及到中文文本处理，
    所以最好是False,本tweet数据集已经全是小写可设为True
    '''    
    #tfidf_matrix = tfidf_vectorizer.fit_transform(tweets_list)
    #上面一行代码等价于下面两行代码
    tfidf_vectorizer.fit(tweets_list)
    tfidf_matrix = tfidf_vectorizer.transform(tweets_list)
#    joblib.dump(tfidf_matrix, 'tfidf_matrix.pkl')
#    tfidf_matrix = joblib.load('tfidf_matrix.pkl')
    
if __name__ == "__main__":
     main()
    
