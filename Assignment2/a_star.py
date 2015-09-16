import csv
import argparse

# Nodes in the search tree created by A*
class Node:
	def __init__(self,world,location,heuristic):
		self.location = location
		if heuristic == 1:
			self.heuristic = heuristic_1(goal(world),location)
		self.f = None
		self.parent = None

# Returns a matrix representation of the world given by file f.
def matrix_of_file(f):
	mat = []
	for line in f:
		mat.append(line[0:-1].split(" "))
	return mat[0:-1]

# Returns the goal square of the world
def goal(world):
	return [len(world[0])-1,0]

# Returns the start square of the world
def start(world):
	return [0,len(world)-1]

# Returns a list of all adjacent squares to the given square
def adjacent(world,x,y):
	adj = []
	for i in range(x-1,x+2):
		if (i >= 0) and (i < len(world[0])):
			if (y-1 >= 0) and (y-1 < len(world)):
				adj.append([i,y-1])
			if (y+1 >= 0) and (y+1 < len(world)):
				adj.append([i,y+1])
	if (x+1 >= 0) and (x+1 < len(world[0])):
		adj.append([x+1,y])
	if (x-1 >= 0) and (x-1 < len(world[0])):
		adj.append([x-1,y])
	return adj

# Heuristic 1 is manhattan distance.
def heuristic_1(goal,square):
	return abs(goal[0] - square[0]) + abs(goal[1] - square[1])

def cost(l,d):
	if world[d[1]][d[0]] == '2':
		return float('inf')
	if ((d[0] == l[0]+1 and d[1] == l[1]+1) or
	   (d[0] == l[0]-1 and d[1] == l[1]-1) or
	   (d[0] == l[0]-1 and d[1] == l[1]+1) or
	   (d[0] == l[0]+1 and d[1] == l[1]-1)):
		tc = 14
	else:
		tc = 10
	if world[d[1]][d[0]] == '1':
		tc = tc + 10
	return tc

def f(cost,heuristic):
	return cost + heuristic

def astar(world,heuristic):
	# Setup
	openset = {}
	closedset = {}
	startnode = Node(world,start(world),heuristic)
	startnode.f = f(0,startnode.heuristic)
	openset[(start(world)[0],start(world)[1])] = startnode
	done = False
	# find the minimum f in the adjacent set
	while openset != {} and not done:
		fmin = float('inf')
		node = None
		node_n = None
		for n in openset.keys():
			if (openset[n]).f < fmin:
				node = openset[n]
				node_n = n
		# If we didn't find a minimum f, then we can't move anywhere.
		if node == None:
			print("No solution was found!")
			return None
		# Remove minimum f from openset
		del openset[node_n]
		closedset[node_n] = node
		# If we have added the goal node to the closed set, then
		# we are done. Stop the algorithm and return the closed set.
		if node.location == goal(world):
			done = True
		# compute adjacent nodes to minimum f
		else:
			adjacentnodes = []
			for l in adjacent(world,node.location[0],node.location[1]):
				newnode = Node(world,l,heuristic)
				newnode.f = f(cost(node.location,l),newnode.heuristic)
				adjacentnodes.append(newnode)
			# Check whether we need to add adjacent nodes to
			# open set or not
			for n in adjacentnodes:
				if (n.location[0],n.location[1]) in openset:
					if n.f <= (openset[(n.location[0],n.location[1])]).f:
						(openset[(n.location[0],n.location[1])]).f = n.f
					(openset[(n.location[0],n.location[1])]).parent = node
				else:
					if (n.location[0],n.location[1]) not in closedset:
						openset[(n.location[0],n.location[1])] = n
	# If we made it out of the loop, we found a solution!
	print("A solution was found!")
	return closedset[(goal(world)[0],goal(world)[1])]

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--f", help="txt file containing world data",
		                   type=str, default="none.txt", required=True)
	argparser.add_argument("--h", help="heuristic function (1 or 2)",
		                   type=int, default=1, required=True)

	args = argparser.parse_args()
	world = matrix_of_file(open(args.f))

	cs = astar(world,args.h)
	print(cs)