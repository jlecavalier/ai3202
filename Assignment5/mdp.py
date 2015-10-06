import csv
import argparse
import random

# Action macros
NOTHING = 'nothing'
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

# Node type macros
EMPTY = '0'
MOUNTAIN = '1'
WALL = '2'
SNAKE = '3'
BARN = '4'
APPLE = '50'

# Discount factor macro
DISCOUNT = 0.9

# States represent each square of the map
class State:
	def __init__(self,location,value):
		# Where is this square?
		self.location = location
		# What is in this square?
		self.value = value
		# How good would it be to move here?
		self.utility = 0
		# How much will I be rewarded for moving here?
		self.reward = get_reward(value)
		# Which squares are next to me?
		self.adjacent = []
		# What should I do at this square?
		self.action = NOTHING

# Returns the reward for moving to a square with the given value
def get_reward(value):
	if value == EMPTY:
		return 0
	if value == MOUNTAIN:
		return -1
	if value == SNAKE:
		return -2
	if value == BARN:
		return 1
	if value == WALL:
		return 0
	if value == APPLE:
		return 50

# Returns a matrix representation of the world given by file f.
def matrix_of_file(f):
	mat = []
	for line in f:
		mat.append(line[0:-1].split(" "))
	return mat[0:-1]

def generate_world(mat):
	world = []
	for i in range(len(mat)):
		world.append(list())
		for j in range(len(mat[0])):
			world[i].append(State([i,j],mat[i][j]))

	for ii in world:
		for jj in ii:
			jj.adjacent = adjacent(jj.location,world)

	return world

# Returns the start square of the world
def start(world):
	return [len(world)-1,0]

def goal(world):
	return [0,len(world[0])-1]

# Returns a list of all adjacent squares to the given square
def adjacent(location,world):
	adj = []
	x = location[0]
	y = location[1]
	if x-1 >= 0:
		if (world[x-1][y]).value != WALL:
			adj.append(world[x-1][y])
	if x+1 < len(world):
		if (world[x+1][y]).value != WALL:
			adj.append(world[x+1][y])
	if y-1 >= 0:
		if (world[x][y-1]).value != WALL:
			adj.append(world[x][y-1])
	if y+1 < len(world[0]):
		if (world[x][y+1]).value != WALL:
			adj.append(world[x][y+1])
	return adj

def get_action_vec(state,world):
	action = NOTHING
	max_expected_util = float('-inf')
	r = state.location[0]
	c = state.location[1]
	# LEFT
	bigsum = 0
	if c-1 >= 0:
		if world[r][c-1] in state.adjacent:
			bigsum += 0.8 * world[r][c-1].utility
		else:
			bigsum += 0.8 * world[r][c].utility
	else:
		bigsum += 0.8 * world[r][c].utility
	if r+1 < len(world):
		if world[r+1][c] in state.adjacent:
			bigsum += 0.1 * world[r+1][c].utility
		else:
			bigsum += 0.1 * world[r][c].utility
	else:
		bigsum += 0.1 * world[r][c].utility
	if r-1 >= 0:
		if world[r-1][c] in state.adjacent:
			bigsum += 0.1 * world[r-1][c].utility
		else:
			bigsum += 0.1 * world[r][c].utility
	else:
		bigsum += 0.1 * world[r][c].utility
	if bigsum >= max_expected_util:
		max_expected_util = bigsum
		action = LEFT

	# RIGHT
	bigsum = 0
	if c+1 < len(world[0]):
		if world[r][c+1] in state.adjacent:
			bigsum += 0.8 * world[r][c+1].utility
		else:
			bigsum += 0.8 * world[r][c].utility
	else:
		bigsum += 0.8 * world[r][c].utility
	if r+1 < len(world):
		if world[r+1][c] in state.adjacent:
			bigsum += 0.1 * world[r+1][c].utility
		else:
			bigsum += 0.1 * world[r][c].utility
	else:
		bigsum += 0.1 * world[r][c].utility
	if r-1 >= 0:
		if world[r-1][c] in state.adjacent:
			bigsum += 0.1 * world[r-1][c].utility
		else:
			bigsum += 0.1 * world[r][c].utility
	else:
		bigsum += 0.1 * world[r][c].utility
	if bigsum >= max_expected_util:
		max_expected_util = bigsum
		action = RIGHT

	# DOWN
	bigsum = 0
	if r+1 < len(world):
		if world[r+1][c] in state.adjacent:
			bigsum += 0.8 * world[r+1][c].utility
		else:
			bigsum += 0.8 * world[r][c].utility
	else:
		bigsum += 0.8 * world[r][c].utility
	if c-1 >= 0:
		if world[r][c-1] in state.adjacent:
			bigsum += 0.1 * world[r][c-1].utility
		else:
			bigsum += 0.1 * world[r][c].utility
	else:
		bigsum += 0.1 * world[r][c].utility
	if c+1 < len(world[0]):
		if world[r][c+1] in state.adjacent:
			bigsum += 0.1 * world[r][c+1].utility
		else:
			bigsum += 0.1 * world[r][c].utility
	else:
		bigsum += 0.1 * world[r][c].utility
	if bigsum >= max_expected_util:
		max_expected_util = bigsum
		action = DOWN

	# UP
	bigsum = 0
	if r-1 >= 0:
		if world[r-1][c] in state.adjacent:
			bigsum += 0.8 * world[r-1][c].utility
		else:
			bigsum += 0.8 * world[r][c].utility
	else:
		bigsum += 0.8 * world[r][c].utility
	if c-1 >= 0:
		if world[r][c-1] in state.adjacent:
			bigsum += 0.1 * world[r][c-1].utility
		else:
			bigsum += 0.1 * world[r][c].utility
	else:
		bigsum += 0.1 * world[r][c].utility
	if c+1 < len(world[0]):
		if world[r][c+1] in state.adjacent:
			bigsum += 0.1 * world[r][c+1].utility
		else:
			bigsum += 0.1 * world[r][c].utility
	else:
		bigsum += 0.1 * world[r][c].utility
	if bigsum >= max_expected_util:
		max_expected_util = bigsum
		action = UP

	return (max_expected_util, action)



def val_iteration(epsilon,world):
	delta = float('inf')
	first = True
	next_world = []
	for i in range(len(world)):
		next_world.append(list())
		for j in range(len(world[0])):
			next_world[i].append(world[i][j].utility)
	while delta > epsilon * ((1 - DISCOUNT)/DISCOUNT):
		delta = 0.0
		for i in range(len(world)):
			for j in range(len(world[0])):
				action_vec = get_action_vec(world[i][j],world)
				#print("Action vec: %4f , %s" % (action_vec[0],action_vec[1]))
				#print ("Prev utility: %4f" % (world[i][j].utility))
				next_world[i][j] = world[i][j].reward + (DISCOUNT * action_vec[0])
				#print ("Next utility: %4f" % (world[i][j].reward + (DISCOUNT * action_vec[0])))
				#print ("Prev utility: %4f" % (world[i][j].utility))
				world[i][j].action = action_vec[1]
				#print("Error: %4f" % abs(next_world[i][j]-world[i][j].utility))
				if abs(world[i][j].utility - next_world[i][j]) > delta:
					delta = abs(world[i][j].utility - next_world[i][j])
					#print("new delta: %d\n\n" % delta)
		#print(next_world)
		for i in range(len(world)):
			for j in range(len(world[0])):
				world[i][j].utility = next_world[i][j]
				#print(world[i][j].utility)
	return world

def display_results(world):
	starts = start(world)
	goals = goal(world)
	state = world[starts[0]][starts[1]]
	print("Optimal path found!\n\n")
	while state != world[goals[0]][goals[1]]:
		print("Location: (%d,%d)\nUtility: %.4f\nAction: %s\n\n" % (state.location[0],state.location[1],state.utility,state.action))
		if state.action == LEFT:
			state = world[state.location[0]][state.location[1]-1]
		elif state.action == RIGHT:
			state = world[state.location[0]][state.location[1]+1]
		elif state.action == UP:
			state = world[state.location[0]-1][state.location[1]]
		elif state.action == DOWN:
			state = world[state.location[0]+1][state.location[1]]


if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--f", help="txt file containing world data",
		                   type=str, default="none.txt", required=True)
	argparser.add_argument("--e", help="epsilon value",
		                   type=int, default=0.5, required=False)

	args = argparser.parse_args()

	w_mat = matrix_of_file(open(args.f))
	world = generate_world(w_mat)

	world = val_iteration(args.e,world)

	display_results(world)