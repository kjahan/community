Community detection for weighted graphs
=======================================
Input: 
A weighted graph G. See graph.txt as a sample for the input graph format. It's a csv file where each line has the following format: 

u,v,w 

The above line specifies that there is an edge between node u and node v with positive weight w. 
The lowest id should be zero and the nodes ids increase. If you want to used this code for an unweighted graph, 
simply set the weight parameter equal to one in each input line.

Output:
This code runs Girvan-Newman algorithm and returns a list of detected community with maximum modularity.

Dependencies:
For running the python code you need to install Python 2.7 and NetworkX package on your machine. Check link below for more details:
http://networkx.github.io/

Girvan-Newman Algorithm Description:
You can find the details of Girvan-Newman algorithm from the following link: 

http://www.kazemjahanbakhsh.com/codes/cmty.html

How to run the Python script:
python cmty.py graph.txt

If you have any question about the code, contact me @ <b>k DOT jahanbakhsh AT gmail DOT com</b>.
