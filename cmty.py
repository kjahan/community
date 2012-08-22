#!/usr/bin/env python
import networkx as nx
import pkg_resources
pkg_resources.require("matplotlib")
import matplotlib.pylab as plt
import math
import csv
import random as rand

def buildG( G, file_, delimiter_ ):
    #construct the weighted version of the contact graph from cgraph.dat file
    #reader = csv.reader(open("/home/kazem/Data/UCI/karate.txt"), delimiter=" ")
    reader = csv.reader(open(file_), delimiter=delimiter_)
    for line in reader:
        if float(line[2]) != 0.0:
            G.add_edge(int(line[0])-1,int(line[1])-1,weight=float(line[2]))

#Keep removing edges from Graph until one of the connected components of Graph splits into two.
#compute the edge betweenness
def CmtyGirvanNewmanStep( G ):
	#print "call CmtyGirvanNewmanStep"
	init_ncomp = nx.number_connected_components(G)	#no of components
	ncomp = init_ncomp
	while ncomp <= init_ncomp:
		bw = nx.edge_betweenness_centrality(G)	#edge betweenness for G
		#find the edge with max centrality
		max_ = 0.0
		#find the edge with the highest centrality and remove all of them if there is more than one!
		for k, v in bw.iteritems():
			#print v
			_BW = float(v)/float(G[k[0]][k[1]]['weight'])	#weighted version of betweenness	
			if _BW >= max_:
				max_ = _BW
		for k, v in bw.iteritems():
			if float(v)/float(G[k[0]][k[1]]['weight']) == max_:
				#print "remove an edge!"
				#print k
				G.remove_edge(k[0],k[1])	#remove the central edge
		ncomp = nx.number_connected_components(G)	#recalculate the no of components

#bw = nx.edge_betweenness_centrality(G)	#edge betweenness for G
#for k, v in bw.iteritems():
	#print v

def _GirvanNewmanGetModularity( G, deg_):
	New_A = nx.adj_matrix(G)
	New_deg = {}
	#print 'inside _GirvanNewmanGetModularity'
	#print deg_
	UpdateDeg(New_deg, New_A)
	#print 'inside _GirvanNewmanGetModularity'
	#print deg_
	#Let's compute the Q
	comps = nx.connected_components(G)	#list of components
	
	print 'no of comp: %d' % len(comps)
	Mod = 0	#Modularity of a given partitionning
	for c in comps:
		EWC = 0	#no of edges within a community
		RE = 0	#no of random edges
        #print "debug: New deg -->"
        print New_deg
        for u in c:
            print "debug: u"
            print u
            EWC += New_deg[u]
			#EWC += G.degree( u )	#let's count the total edges which fall within a community
            RE += deg_[u]		#count the probability of a random edge
        Mod += ( float(EWC) - float(RE*RE)/float(2*m_) )
    Mod = Mod/float(2*m_)
    #print "Modularity: %f" % Mod
    #return Mod

def UpdateDeg(deg_, A_):
	#print 'before, inside UpdateDeg'
	#print deg_
	for i in range(0,n):
		deg = 0.0
		for j in range(0,n):
			#if i == 0:
				#print '%d %d %d' % (i,j,A[i,j])
			deg += A_[i,j]
		deg_[i] = deg
	#print 'after, inside UpdateDeg'
	#print deg_	
	#print deg_

#Q = 0.0
#for u in G.nodes():
	#for v in G.nodes():
		#if u in nx.node_connected_component(G, v):
			##print '%d and %d have the same component --> %d, %d, %d, %d' % (u,v, A[u,v], deg_[u], deg_[v], m_)
			#Q += float(A[u,v])/float(2*m_) - float(deg_[u]*deg_[v])/float(math.pow(2*m_,2))
			##print Q
			
#print "Q: %f" % Q
#print nx.laplacian_spectrum(G)	
G = nx.Graph()
buildG(G, '/Users/kazemjahanbakhsh/Downloads/graph.txt', ',')

n = G.number_of_nodes()	#|V|
print G.nodes()
#m_ = G.number_of_edges()	#|E|
print 'no of nodes: %d' % n

f_gl = open('/Users/kazemjahanbakhsh/Downloads/community/Glap.dat', 'w')
Glap = nx.normalized_laplacian(G)
for i in range(0,n):
	val = ''
	for j in range(0,n):
		val += str(Glap[i,j])
		if j < n-1:
			val += ','
	val += '\n'
	f_gl.write(val)
f_gl.close()		

A = nx.adj_matrix(G)
#for i in range(0,10):
	#print A[0,i]

m_ = 0.0	#the weighted version for number of edges
for i in range(0,n):
	for j in range(0,n):
		m_ += A[i,j]
m_ = m_/2.0
print "m: %f" % m_

#deg_ = G.degree()
#calculate the weighted degree for each node
Orig_deg = {}
UpdateDeg(Orig_deg, A)
	
nx.draw_spring(G,
		node_color=[float(G.degree(v)) for v in G],
		node_size=40,
		with_labels=False,
		cmap=plt.cm.Reds,
		)
#plt.show()
	
BestQ = 0.0
Q = 0.0
while True:	
	CmtyGirvanNewmanStep(G)
	Q = _GirvanNewmanGetModularity(G, Orig_deg);
	print "current modularity: %f" % Q
	if Q > BestQ:
		BestQ = Q
		Bestcomps = nx.connected_components(G)	#Best Split
		print "comps:"
		print Bestcomps
		H = nx.connected_component_subgraphs(G)[1]
		Hlap = nx.normalized_laplacian(H)
		#CmtyV.Swap(CurCmtyV);
	#if (Cmty1.Len()==0 || Cmty2.Len() == 0) { break; }
	#when should we stop splitting the graph?
	if G.number_of_edges() == 0:
		break
if BestQ > 0.0:
	size = Hlap.shape
	
	f_hl = open('/home/kazem/Hlap.dat', 'w')
	for i in range(0,size[0]):
		val = ''
		for j in range(0,size[1]):
			val += str(Hlap[i,j])
			if j < size[1] - 1:
				val += ','
		val += '\n'
		f_hl.write(val)
	f_hl.close()

	print "Best Q: %f" % BestQ
	print Bestcomps
else:
	print "Best Q: %f" % BestQ
#nx.draw_spring(G,
		#node_color=[float(G.degree(v)) for v in G],
		#node_size=40,
		#with_labels=False,
		#cmap=plt.cm.Reds,
		#)
#plt.show()