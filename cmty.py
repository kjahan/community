#!/usr/bin/env python
import networkx as nx
import pkg_resources
pkg_resources.require("matplotlib")
import matplotlib.pylab as plt
import math
import csv
import random as rand

#this method just reads the graph structure from the file
def buildG( G, file_, delimiter_ ):
    #construct the weighted version of the contact graph from cgraph.dat file
    #reader = csv.reader(open("/home/kazem/Data/UCI/karate.txt"), delimiter=" ")
    reader = csv.reader(open(file_), delimiter=delimiter_)
    for line in reader:
        if float(line[2]) != 0.0:
            G.add_edge(int(line[0]),int(line[1]),weight=float(line[2]))

#Keep removing edges from Graph until one of the connected components of Graph splits into two.
#compute the edge betweenness
def CmtyGirvanNewmanStep( G ):
    #print "call CmtyGirvanNewmanStep"
    init_ncomp = nx.number_connected_components(G)    #no of components
    ncomp = init_ncomp
    while ncomp <= init_ncomp:
        bw = nx.edge_betweenness_centrality(G)    #edge betweenness for G
        #find the edge with max centrality
        max_ = 0.0
        #find the edge with the highest centrality and remove all of them if there is more than one!
        for k, v in bw.iteritems():
            _BW = float(v)/float(G[k[0]][k[1]]['weight'])    #weighted version of betweenness    
            if _BW >= max_:
                max_ = _BW
        for k, v in bw.iteritems():
            if float(v)/float(G[k[0]][k[1]]['weight']) == max_:
                G.remove_edge(k[0],k[1])    #remove the central edge
        ncomp = nx.number_connected_components(G)    #recalculate the no of components
#compute the modularity of current split
def _GirvanNewmanGetModularity( G, deg_):
    New_A = nx.adj_matrix(G)
    New_deg = {}
    UpdateDeg(New_deg, New_A)
    #Let's compute the Q
    comps = nx.connected_components(G)    #list of components    
    print 'no of comp: %d' % len(comps)
    Mod = 0    #Modularity of a given partitionning
    for c in comps:
        EWC = 0    #no of edges within a community
        RE = 0    #no of random edges
        for u in c:
            EWC += New_deg[u]
            RE += deg_[u]        #count the probability of a random edge
        Mod += ( float(EWC) - float(RE*RE)/float(2*m_) )
    Mod = Mod/float(2*m_)
    #print "Modularity: %f" % Mod
    return Mod

def UpdateDeg(deg_, A_):
    for i in range(0,n):
        deg = 0.0
        for j in range(0,n):
            deg += A_[i,j]
        deg_[i] = deg

#let's create a graph and insert the edges
G = nx.Graph()
buildG(G, 'graph.txt', ',')

n = G.number_of_nodes()    #|V|
#adjacenct matrix
A = nx.adj_matrix(G)

m_ = 0.0    #the weighted version for number of edges
for i in range(0,n):
    for j in range(0,n):
        m_ += A[i,j]
m_ = m_/2.0
print "m: %f" % m_

#calculate the weighted degree for each node
Orig_deg = {}
UpdateDeg(Orig_deg, A)

#let's find the best split of the graph
BestQ = 0.0
Q = 0.0
while True:    
    CmtyGirvanNewmanStep(G)
    Q = _GirvanNewmanGetModularity(G, Orig_deg);
    print "current modularity: %f" % Q
    if Q > BestQ:
        BestQ = Q
        Bestcomps = nx.connected_components(G)    #Best Split
        print "comps:"
        print Bestcomps
    if G.number_of_edges() == 0:
        break
if BestQ > 0.0:
    print "Best Q: %f" % BestQ
    print Bestcomps
else:
    print "Best Q: %f" % BestQ