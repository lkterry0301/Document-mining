print 'CSE 5243 Similarity Matrix by Kun Liu & Zhe Dong'

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--file", dest="in_file",
		 help="the input vector",metavar="FILE")
parser.add_option("-o", "--output", dest="out_file",
		  help="the output matrix file", metavar="FILE")
parser.add_option("-a", "--algorithm", dest="algorithm",
		  metavar="[Euclidean|Other]",
		 default="Euclidean", help="Type of similarity")
(options, args) = parser.parse_args()


#### put a vector file definition here

#open vector file
vector_file = open(options.in_file, 'r')

#read vector into classes
import ast
import sys
L = []
print "Reading vectors... ",
sys.stdout.flush()
for line in vector_file:
	data = ast.literal_eval(line);
	L.append(data)
print "done"

#compute the pairwise distance
import distance
dist_func = {
	'euclidean':distance.euclidean_sparse
}
func = dist_func[(options.algorithm.lower())]
D_Matrix = []
for i in range(0, len(L)-1):
	v = []
	for j in range(0, i):
		d = func(L[i], L[j])
		v.append(d)
	D_Matrix.append(v)

#encode the matrix and save

out = open("result.txt",'w')
print >>f, D_Matrix

#TODO:
#1. measure time
#2. put paser code into another file
