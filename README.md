# ai3202
Implementation of the A* algorithm for CSCI 3202

# My custom heuristic function:
My heuristic is not represented by a simple mathematical formula. However, I can still explain what it does rigorously. The idea of my heuristic is to count the number of obstacles between the horse and the goal. The heuristic first creates a 'box'. This box contains all the squares above and to the right of the horse. Then, the heuristic loops through all of the squares inside the boundary of the box and adds one for each mountain and two for each wall. After this, it returns the total sum.

# Why my heuristic is reasonable
My heuristic should work well because it only considers squares inside the box it creates, which are squares that are closer (in terms of Manhattan distance) to the goal than the current position. In addition, it creates a heavier cost for more obstacles. Mountains count less than walls because mountains can still be walked through, even though they cost more than empty squares. This has the effect of the algorithm generally avoiding rectangular areas of the maze that have lots of obstacles in them.

# How my heuristic compares to Manhattan distance
Generally, my heuristic performs better than Manhattan distance. It always finds a path with the same cost as the Manhattan distance, but it also evaluates fewer nodes along the way. Here are the data to prove this:

For world 1, the results are as follows:
MANHATTAN DISTANCE:
heuristic: 1
62 nodes evaluated
Path:
[0, 7]
[1, 7]
[2, 7]
[3, 6]
[3, 5]
[4, 4]
[5, 3]
[6, 3]
[7, 2]
[7, 1]
[8, 0]
[9, 0]
130 for cost

MY HEURISTIC:
58 nodes evaluated
path:
[0, 7]
[1, 7]
[2, 7]
[3, 6]
[3, 5]
[4, 4]
[5, 3]
[6, 3]
[7, 3]
[8, 2]
[9, 1]
[9, 0]
130 for cost

For world 2, the results are as follows:
MANHATTAN DISTANCE:
60 nodes evaluated
path:
[0, 7]
[1, 7]
[2, 7]
[3, 6]
[3, 5]
[3, 4]
[4, 3]
[4, 2]
[4, 1]
[5, 0]
[6, 0]
[7, 0]
[8, 0]
[9, 0]
142 for cost

MY HEURISTIC:
54 nodes evaluated
path:
[0, 7]
[1, 7]
[2, 7]
[3, 6]
[3, 5]
[3, 4]
[4, 3]
[4, 2]
[4, 1]
[5, 0]
[6, 0]
[7, 0]
[8, 0]
[9, 0]
142 for cost
