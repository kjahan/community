import networkx as nx
import csv
import sys

DEBUG = False

# This method reads the graph structure from the input file
def buildG(G, file_, delimiter_):
    # construct the weighted version of the contact graph from the input file
    with open(file_, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter_)
        for line in reader:
            if len(line) > 2:
                if float(line[2]) != 0.0:
                    # line format: u,v,w
                    G.add_edge(int(line[0]), int(line[1]), weight=float(line[2]))
            else:
                # line format: u,v
                G.add_edge(int(line[0]), int(line[1]), weight=1.0)


# This method keeps removing edges from Graph until one of the connected components of Graph splits into two
# compute the edge betweenness
def cmtyGirvanNewmanStep(G):
    if DEBUG:
        print("Running cmtyGirvanNewmanStep method ...")
    init_ncomp = nx.number_connected_components(G)  # no of components
    ncomp = init_ncomp
    while ncomp <= init_ncomp:
        bw = nx.edge_betweenness_centrality(G, weight='weight')  # edge betweenness for G
        # find the edge with max centrality
        max_ = max(bw.values())
        # find the edge with the highest centrality and remove all of them if there is more than one!
        for k, v in bw.items():
            if v == max_:
                G.remove_edge(*k)  # remove the central edge
        ncomp = nx.number_connected_components(G)  # recalculate the no of components


# This method compute the modularity of current split
def girvanNewmanGetModularity(G, deg_, m_):
    New_A = nx.adjacency_matrix(G)
    New_deg = updateDeg(New_A, G.nodes())
    # Let's compute Q
    comps = nx.connected_components(G)  # list of components
    print('No of communities in decomposed G: {}'.format(nx.number_connected_components(G)))
    Mod = 0  # Modularity of a given partitioning
    for c in comps:
        EWC = 0  # no of edges within a community
        RE = 0  # no of random edges
        for u in c:
            EWC += New_deg[u]
            RE += deg_[u]  # count the probability of a random edge
        Mod += (EWC - RE * RE / (2 * m_))
    Mod = Mod / (2 * m_)
    if DEBUG:
        print("Modularity: {}".format(Mod))
    return Mod


def updateDeg(A, nodes):
    deg_dict = {}
    n = len(nodes)
    B = A.sum(axis=1)
    for i, node_id in enumerate(nodes):
        deg_dict[node_id] = B[i, 0]
    return deg_dict


# This method runs Girvan-Newman algorithm and finds the best community split by maximizing the modularity measure
def runGirvanNewman(G, Orig_deg, m_):
    # Let's find the best split of the graph
    BestQ = 0.0
    Q = 0.0
    while True:
        cmtyGirvanNewmanStep(G)
        Q = girvanNewmanGetModularity(G, Orig_deg, m_)
        print("Modularity of decomposed G: {}".format(Q))
        if Q > BestQ:
            BestQ = Q
            Bestcomps = list(nx.connected_components(G))  # Best Split
            print("Identified components: {}".format(Bestcomps))
        if G.number_of_edges() == 0:
            break
    if BestQ > 0.0:
        print("Max modularity found (Q): {} and number of communities: {}".format(BestQ, len(Bestcomps)))
        print("Graph communities: {}".format(Bestcomps))
    else:
        print("Max modularity (Q):", BestQ)


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <input graph>\n" % (argv[0],))
        return 1
    graph_fn = argv[1]
    G = nx.Graph()  # let's create the graph first
    buildG(G, graph_fn, ',')

    if DEBUG:
        print('G nodes: {} & G no of nodes: {}'.format(G.nodes(), G.number_of_nodes()))

    n = G.number_of_nodes()  # |V|
    A = nx.adjacency_matrix(G)  # adjacency matrix

    m_ = 0.0  # the weighted version for the number of edges
    for i in range(0, n):
        for j in range(0, n):
            m_ += A[i, j]
    m_ = m_ / 2.0
    if DEBUG:
        print("m: {}".format(m_))

    # calculate the weighted degree for each node
    Orig_deg = updateDeg(A, G.nodes())

    # run Girvan-Newman algorithm
    runGirvanNewman(G, Orig_deg, m_)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
