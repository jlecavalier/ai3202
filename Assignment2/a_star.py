import csv
import argparse

# Nodes in the search tree created by A*
class Node:
	def __init__(self,world,location,heuristic):
		self.location = location
		if heuristic == 1:
			self.heuristic = heuristic_1(goal(world),location)
		if heuristic == 2:
			self.heuristic = heuristic_2(world,location)
		self.f = None
		self.g = 0
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

# For now, heuristic_2 just causes the algorithm to reduce to Dijkstra's algorithm
def heuristic_2(world,square):
	return 0

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
			if (openset[n]).f <= fmin:
				node = openset[n]
				node_n = n
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
				newnode.g = node.g + cost(node.location,l)
				newnode.f = f(newnode.g,newnode.heuristic)
				adjacentnodes.append(newnode)
			# Check whether we need to add adjacent nodes to
			# open set or not
			for n in adjacentnodes:
				# If the node we're evaluating is a wall or it is already
				# in the closed set, we don't need to evaluate it at all.
				if ((n.location[0],n.location[1]) not in closedset) and (world[n.location[1]][n.location[0]] != '2'):
					# If the node we're evaluating isn't in the open set,
					# add it to the open set and set its parent to the current
					# node.
					if (n.location[0],n.location[1]) not in openset:
						openset[(n.location[0],n.location[1])] = n
						n.parent = node
					# If the node we're evaluating is already in the open set,
					# then check if the cost of getting to that node from the
					# current node is less than the cost already calculated
					# for that node. If it is, update accordingly.
					else:
						if n.g < (openset[(n.location[0],n.location[1])]).g:
							(openset[(n.location[0],n.location[1])]).g = n.g
							(openset[(n.location[0],n.location[1])]).f = n.f
							(openset[(n.location[0],n.location[1])]).parent = node
	# If we made it out of the loop, we found a solution!
	if (goal(world)[0],goal(world)[1]) in closedset:
		print("A solution was found!\n")
		print("Number of locations evaluated:")
		print(len(closedset))
		return closedset[(goal(world)[0],goal(world)[1])]
	else:
		print("No solution was found!")
		return None

def calculate_results(goal):
	if goal == None:
		print("\nI'm so sad now :(")
	else:
		pathlist_reversed = []
		curr = goal
		while curr != None:
			pathlist_reversed.append(curr)
			curr = curr.parent
		pathlist = pathlist_reversed[::-1]
		print("\nPath taken:")
		for i in range(len(pathlist)):
			print(pathlist[i].location)
		print("\nCost of path")
		print(goal.g)
		print("")


if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--f", help="txt file containing world data",
		                   type=str, default="none.txt", required=True)
	argparser.add_argument("--h", help="heuristic function (1 or 2)",
		                   type=int, default=1, required=True)

	args = argparser.parse_args()
	world = matrix_of_file(open(args.f))

	cs = astar(world,args.h)
	calculate_results(cs)