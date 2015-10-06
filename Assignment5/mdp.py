import csv
import argparse
import random

# Action macros
NOTHING = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

# Node type macros
EMPTY = 0
MOUNTAIN = 1
WALL = 2
SNAKE = 3
BARN = 4
APPLE = 50

# Discount factor macro
DISCOUNT = 0.9

# Global world variable
world = []

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
	for i in range(len(mat[0])):
		for j in range(len(mat)):
			world[i][j] = State([i,j],mat[i][j])

	for ii in world:
		ii.adjacent = adjacent(ii.location)

# Returns the start square of the world
def start(world):
	return [0,len(world)-1]

# Returns a list of all adjacent squares to the given square
def adjacent(location):
	adj = []
	x = location[0]
	y = location[1]
	if x-1 >= 0:
		if (world[x-1][y]).value != WALL:
			adj.append(world[x-1][y])
	if x+1 < len(world[0]):
		if (world[x+1][y]).value != WALL:
			adj.append(world[x+1][y])
	if y-1 >= 0:
		if (world[x][y-1]).value != WALL:
			adj.append(world[x][y-1])
	if y+1 < len(world):
		if (world[x][y+1]).value != WALL:
			adj.append(world[x][y+1])
	return adj

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--f", help="txt file containing world data",
		                   type=str, default="none.txt", required=True)
	argparser.add_argument("--e", help="epsilon value",
		                   type=int, default=0.5, required=False)

	args = argparser.parse_args()

	w_mat = matrix_of_file(open(args.f))
	generate_world(w_mat)