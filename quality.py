# -*- coding: utf-8 -*-
"""
@author: Kun Liu, Zhe Dong

"""

import math
import numpy
from scipy.spatial import distance

#calculate entropy for one cluster
def cluster_entropy(class_in_cluster):
    total_entropy=0
    total=sum(class_in_cluster.values())
    
    for i in class_in_cluster:
        probability = (0.0+class_in_cluster[i]) / total
        
        entropy = probability * math.log(probability,2)
        total_entropy += entropy
    
    return -1 * total_entropy


def get_cluster_size(clustered_vector):
    cluster_sizes=[]
    for cluster in clustered_vector:
        cluster_sizes.append(len(cluster))
    return cluster_sizes

#get centroid of one cluster
def cluster_centroid(one_cluster):
    centroid = [0]*len(one_cluster[0])
    
    #sum up one cluster
    for vector in one_cluster:
        for i in range (0, len(centroid)):
            centroid[i] += vector[i]
    
    #get average
    for j in range(0,len(centroid)):
        centroid[j] = centroid[j] / len(one_cluster)
    
    return centroid
    
def cluster_radius(one_cluster, centroid):
    sum_distance = 0
    for vector in one_cluster:
        sum_distance += distance.euclidean(vector,centroid)
        
    radius=sum_distance/(2*len(one_cluster))
    return radius
            
def cluster_SSE(one_cluster, centroid):
    SSE=0
    for vector in one_cluster:
        SSE+=(distance.euclidean(vector,centroid))^2
    return SSE
    
#prediction is predicted index of each data from clustering model
#word_vector is feature vectors used in clustering
#class_label_vector is the topic labels for each feature vector (article)

def quality_evaluation(prediction, word_vector, class_label_vector):
    
    #get n_cluster
    n_clusters = max(prediction)+1
    print "Total number of clusters is "+str(n_clusters)
    
    #partition vector data into each cluster
    clustered_vector=[]
    for i in range(0,n_clusters):
        clustered_vector.append([])
    
    for j in range(0,len(word_vector)):
        clustered_vector[prediction[j]].append(word_vector[j])
    
    #counts class (topic) labels in each cluster
    class_in_cluster=[] #class counts in each cluster
    total_class_count={}
    for k in range(0,n_clusters):
        class_in_cluster.append({})
    
    for l in range(0,len(prediction)):
        for label in class_label_vector[l]:
            #add class label to each cluster
            cluster_class=class_in_cluster[prediction[l]]
            cluster_class[label]=cluster_class.get(label,0) + 1
            #get total counts for each class label
            total_class_count[label]=total_class_count.get(label,0)+1
    
    #calculate entropy for clustering
    entropy_list=[]
    accumulative_entropy=0
    for m in range(0,n_clusters):
        single_entropy=cluster_entropy(class_in_cluster[m])
        entropy_list.append(single_entropy)
        accumulative_entropy+=single_entropy*(0.0+len(clustered_vector[m]))/len(word_vector)
        
    non_cluster_entropy=cluster_entropy(total_class_count)
    information_gain=non_cluster_entropy-accumulative_entropy
    print "Information Gain (IG) :" + str(information_gain)
    
    #get list of prediction size in each cluster
    cluster_sizes=get_cluster_size(clustered_vector)
    #Calculate standard deviation of cluster sizes
    print "Standard deviation of cluster sizes: " +str(numpy.std(cluster_sizes))
    
    #get centroids of cluster
    centroids = []
    for cluster in clustered_vector:
        centroids.append(cluster_centroid(cluster))
    
    #Calculate cluster radiuses and SSE
    cluster_radiuses=[]
    cluster_SSEs=[]
    
    for p in range(0,n_clusters):
        cluster_radiuses.append(cluster_radius(clustered_vector[p],centroids[p]))
        cluster_SSEs.append(cluster_SSE(clustered_vector[p],centroids[p]))
    
    #get average cluster radius
    avg_radius=sum(cluster_radiuses)/len(cluster_radiuses)
    print "Average radius of cluster is : "+str(avg_radius)
    
    #get average cluster SSE
    avg_SSE=sum(cluster_SSEs)/len(cluster_SSEs)
    print "Average SSE of cluster is : "+str(avg_SSE)
        