from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN

#KMeans clustering function
def kmeans_clustering(n_clusters,word_vector):
  model=KMeans(n_clusters=n_clusters)
  prediction=model.fit_predict(word_vector)
  return prediction
  
#Hierarchical clustering function
def hierarchical_clustering(n_clusters,word_vector,metric,link):
  #affinity is metric used. Can be "euclidean", "l1", "l2", "manhattan", "cosine", or "precomputed". If linkage is "ward", only "euclidean" is accepted.
  #linkage can be {"ward", "complete", "average"}
  model=AgglomerativeClustering(n_clusters=n_clusters,affinity=metric, linkage=link) 
  prediction=model.fit_predict(word_vector)
  return prediction
  
#DBSCAN clustering function
def DBSCAN_clustering(eps,sample_size, word_vector,metric):
  #metrican be "euclidean", "l1", "l2", "manhattan", "cosine", or "precomputed". If linkage is "ward", only "euclidean" is accepted.
  model= DBSCAN(eps=eps,min_samples=sample_size, metric=metric) 
  prediction=model.fit_predict(word_vector)
  return prediction