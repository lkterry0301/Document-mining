print 'CSE 5243 Clustering Analysis by Kun Liu & Zhe Dong'

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--file", dest="in_file",
		 help="the input vector",metavar="FILE",default="vector1.txt")
parser.add_option("-o", "--output", dest="out_file",
		  help="the output matrix file", metavar="FILE")
parser.add_option("-m", "--metric", dest="metric",
		  metavar="[Euclidean|Manhattan]",
		 default="euclidean", help="Type of similarity")
parser.add_option("-a", "--algorithm", dest="algorithm",
		  metavar="[DBSCAN|Hierarchical]",
		  default="DBSCAN")
parser.add_option("-e", "--eps", dest="epsilon", metavar="<Epsilon>",
		  type="float", default=0.5)
parser.add_option("-M", "--min-sample", dest="min_sample", metavar="<Min samples>",
		  type="int", default=5) 
parser.add_option("-t", "--test", dest="small_data",
		  action="store_true", default=False)
parser.add_option("-k", dest="cluster", metavar="<Cluster>", type="int",
		  default=2)
parser.add_option("-l", dest="linkage", metavar="[Ward|Average|Complete]",
		  default="ward")

(options, args) = parser.parse_args()

#open vector file
vector_file = open(options.in_file, 'r')
label_file = open('label.txt', 'r')

#read vector into classes
import ast
import sys
from scipy.sparse import *
info = open("info.txt",'r');
rdim = int(info.readline())
cdim = int(info.readline())


if options.small_data:
	rdim = 1000;
	print 'small test set selected, only loading 1000 rows'

S = lil_matrix((rdim, cdim))

import time
start_time = time.time()

print "Reading vectors... ",
sys.stdout.flush()
i = 0
for line in vector_file:
	data = ast.literal_eval(line);
	for D in data:
		S[i, int(D[0])] = float(D[1])
	i=i+1
	if i==rdim:
		break
label = []
i = 0
for line in label_file:
	label.append(ast.literal_eval(line))
	if i==rdim:
		break

print "done"
S = S.tocsr()

data_process_time= time.time()  - start_time

#choose cluster method
print ("Clustering... ")
import cluster
prediction = []


if options.algorithm.lower()=="dbscan":
    print ("DBSCAN")
    eps=options.epsilon
    min_sample=options.min_sample
    metric=options.metric.lower()
    print ("eps= "+str(eps)+", min_sample= "+str(min_sample)+", metric= "+metric)
    prediction=cluster.DBSCAN_clustering(eps,min_sample,S,metric)
    S=S.toarray()
elif options.algorithm.lower()=="hierarchical":
    S=S.toarray()
    print ("Hierarchical")
    n_clusters=options.cluster
    metric=options.metric.lower()
    link=options.linkage.lower()
    print ("num_cluster= "+str(n_clusters)+", metric= "+metric+", linkage= "+link)
    prediction=cluster.hierarchical_clustering(n_clusters,S,metric,link)

'''
print ("DBSCAN")
eps=0.5
min_sample=10
metric='manhattan'#manhattan
print ("eps= "+str(eps)+", min_sample= "+str(min_sample)+", metric= "+metric)
prediction=cluster.DBSCAN_clustering(eps,min_sample,S,metric)
S=S.toarray()
'''

'''
S=S.toarray()
print ("Hierarchical")
n_clusters=500
metric='euclidean'#manhattan
link='ward'
print ("num_cluster= "+str(n_clusters)+", metric= "+metric+", linkage= "+link)
prediction=cluster.hierarchical_clustering(n_clusters,S,metric,link)
'''

print "done"

clustering_time= time.time()  - start_time - data_process_time

#evaluate result
quality_start_time=time.time()
import quality
quality.quality_evaluation(prediction, S, label)

quality_time=time.time()-quality_start_time
total_time=time.time()-start_time

print ""
print "Running time:"
print "Data processing time: "+str(data_process_time)+" seconds"
print "Clustering time: "+str(clustering_time)+" seconds"
print "Quality evaluation time: "+str(quality_time)+" seconds"
print "Total running time: "+str(total_time)+" seconds"
print ""


#print len(prediction)
#print cluster result
print "Distribution in clusters:"
hist = {}
for item in prediction:
	if item in hist:
		hist[item] += 1
	else:
		hist[item] = 1

for key in hist:
	print key," ", hist[key]
