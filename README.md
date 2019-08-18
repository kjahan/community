![Image description](http://www.lonelyplanet.com/travel-blog/tip-article/wordpress_uploads/2015/04/Istanbul-Grand-Bazaar_CS.jpg)

Detecting Communities in Weighted Graphs
========================================

## Input
 
A weighted graph G. See graph.txt file as a sample for the input graph format. It's a CSV file where each line has the following format: 

	u,v,w 

Above line specifies that there is an edge between node u and v with positive weight w. 
The lowest id should be zero and the nodes id's increase. If you want to used this code for an unweighted graph, 
simply set the weight equal to one on each input line.

## Output

This code runs Girvan-Newman algorithm and returns a list of detected communities with maximum modularity.

## Dependencies

For running the python code, you need to install Python 3 and NetworkX package on your machine. Check link below for more details:

	https://networkx.github.io/documentation/latest/install.html

## Girvan-Newman Algorithm Description

You can find the details for how Girvan-Newman algorithm works from the following link: 

	http://www.kazemjahanbakhsh.com/codes/cmty.html

## How to run Python script

	python cmty.py graph.txt

If you have any question about the code or you want to report a bug, please contact me @ <b>k DOT jahanbakhsh AT gmail DOT com</b>.

## Licence

    Copyright (c) 2013 Black Square Media Ltd. All rights reserved.
    (The MIT License)

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    'Software'), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

