# Jordan Stein
# Artificial Intelligence PA1
# slidingpuzzle.py

# This script reads in different 8-tile puzzles in JSON
# Multiple algorithms are used to solve each puzzle


# data is the puzzle matrix, type denotes 'start' / 'goal' / 'progress'
# Prints the puzzle matrix very prettily 

def printPuzzle(data, type, move=0, direction=''):
	if type == 'start':
		print 'start:'
	elif type == 'goal':
		print 'goal:'

	if move != 0:
		print 'move:', move, direction

	if type == 'start' or type == 'goal':
		for x in range(0,len(data)):
			print str(data[type][x]).replace('[','').replace(']','').replace(',','').replace('0', ' ')
	
	if type == 'progress':
		for x in range(0, len(data)):
			print str(data[x]).replace('[','').replace(']','').replace(',','').replace('0', ' ')

	return


# Ensures that the correct json data was read-in

def validateMatrix(data):
	from sys import exit

	if data['n'] < 1:
		print "Invalid JSON data: n < 1"
	
	validTiles = [] # fills list from (0,1,2,...n-2,n-1)
	for x in range(0, data['n']*data['n']):
		validTiles.append(x)

	# flattens out start matrix and goal matrix
	startData = sum(data['start'], [])
	startData.sort()
	goalData = sum(data['goal'], [])
	goalData.sort()

	# validTiles should = startData and goalData
	# if not, an invalid matrix was given in JSON
	for x in range(0,len(validTiles)):
		if validTiles[x] != startData[x]:
			print "'start' matrix contains invalid tiles."
			exit()
		elif validTiles[x] != goalData[x]:
			print "'goal' matrix contains invalid tiles."
			exit()


# defines the rules allowed for valid moves
# returns a list of valid moves [up, down, left, right]

def rules(puzzle, lastMove=''):
	moves = ['u', 'd', 'l', 'r'] # up down left right

	if lastMove == 'u' and 'd' in moves:
		moves.remove('d')
	if lastMove == 'd' and 'u' in moves:
		moves.remove('u')
	if lastMove == 'l' and 'r' in moves:
		moves.remove('r')
	if lastMove == 'r' and 'l' in moves:
		moves.remove('l')


	# finds the x,y position of empty tile 0
	try:
		for x in range(0, len(puzzle)):
			for y in range(0, len(puzzle)):
				if puzzle[x][y] == 0:
					# breaks out of both loops when 0 is found
					raise StopIteration
	except StopIteration: pass

	if x == 0 and 'u' in moves:
		moves.remove('u')
	if x == len(puzzle)-1 and 'd' in moves:
		moves.remove('d')
	if y == 0 and 'l' in moves:
		moves.remove('l')
	if y == len(puzzle)-1 and 'r' in moves:
		moves.remove('r')

	return moves


# heuristic algorithm
# returns the number of tiles are are in the incorrect place

def h(puzzle):
	incorrect = 0

	count = 0
	for x in range(0, len(puzzle)):
		for y in range(0, len(puzzle)):
			if (count != puzzle[x][y] and puzzle[x][y] != 0):
				incorrect+=1
			count+=1

	return incorrect


# If bestMove is marked True, swaps tile pieces and returns new puzzle
# If bestMove is marked False, simulates a piece swap, returns hueristic value for simulated swap
# move = 'u' , 'd' , 'l' , 'r'

def moveTile(puzzle, move, bestMove = False):

	# finds empty tile, swaps it with determined move [u, d, l, r]
	for x in range(0, len(puzzle)):
		for y in range(0, len(puzzle)):
			if (puzzle[x][y] == 0):
				if move == 'u': # swap empty tile with tile above it
					puzzle[x][y] = puzzle[x-1][y]
					puzzle[x-1][y] = 0

					if bestMove == False:
						heuristic = h(puzzle) # record heuristic value
						puzzle[x-1][y] = puzzle[x][y] # swap tiles back
						puzzle[x][y] = 0
						return heuristic
					else:
						return puzzle

				elif move == 'd': # swap empty tile with tile below it
					puzzle[x][y] = puzzle[x+1][y]
					puzzle[x+1][y] = 0

					if bestMove == False:
						heuristic = h(puzzle) # record heuristic value
						puzzle[x+1][y] = puzzle[x][y] # swap tiles back
						puzzle[x][y] = 0
						return heuristic
					else:
						return puzzle

				elif move == 'l': # swap empty tile with tile to the left
					puzzle[x][y] = puzzle[x][y-1]
					puzzle[x][y-1] = 0

					if bestMove == False:
						heuristic = h(puzzle) # record heuristic value
						puzzle[x][y-1] = puzzle[x][y] # swap tiles back
						puzzle[x][y] = 0
						return heuristic
					else:
						return puzzle

				elif move == 'r': # swap empty tile with tile to the right
					puzzle[x][y] = puzzle[x][y+1]
					puzzle[x][y+1] = 0

					if bestMove == False:
						heuristic = h(puzzle) # record heuristic value
						puzzle[x][y+1] = puzzle[x][y] # swap tiles back
						puzzle[x][y] = 0
						return heuristic
					else:
						return puzzle
	return puzzle


# Solves the puzzle via backtracking AKA
# Depth-first search to attempt all possible move orders
# If the maximum amount of moves are tested with no solution, The
# algorithm will backtrack a state and try the remaining possible moves

def backtracking(puzzle, goal, maxmoves):

	states = []
	movesMade = []
	solution = []
	lastMove = ''
	win = False
	depth = 0
	index = 0
	moveCount = 0
	moveIndex = 0
	backtrack = False


	states.append(copy.deepcopy(puzzle))


	while (not win):

		time.sleep(1) # delay's output so you can visualize the algorithm

		if len(states) == 0:
			states = []
			states.append(copy.deepcopy(puzzle)) # if we get back to initial state, re-initialize it
			backtrack = False
			moveCount = 0
			lastMove = solution.pop() # "first move" we made
			solution = []

		
		moveList = rules(states[len(states)-1], lastMove)

		if not backtrack:
			if lastMove in moveList:
				moveList.remove(lastMove)
			moveIndex = 0
			newPuzzle = moveTile(copy.deepcopy(states[len(states)-1]), moveList[0], True)
			solution.append(moveList[moveIndex])

			backtrack = False
		else:

			moveList = rules(states[len(states)-1])
			print moveList
			newPuzzle = moveTile(copy.deepcopy(states[len(states)-1]), moveList[len(moveList)-1], True)
			solution.append(moveList[moveIndex])
			if newPuzzle != goal:
				backtrack = True

		
		if not backtrack:
			states.append(newPuzzle)
			moveCount +=1

		printPuzzle(states[len(states)-1], 'progress', moveCount, solution[len(solution)-1])
		print moveList
		
		lastMove = solution[len(solution)-1]


		if newPuzzle == goal:
			win = True
			print "SOLVED"
			print "backtracking Solution: ", solution

		if moveCount > maxmoves-1 or backtrack == True:
			print "BACKTRACKING"

			states.pop()
			lastMove = solution.pop()
			#moveIndex+=1
		#	depth-=1
			moveCount-=1
			backtrack = True
			#exit()
			if len(states) == 0:
				backtrack = False
		else:
			backtrack = False



# Solves the puzzle via BRUTE FORCE
# this algorithm tries all possible moves for every state
# It only cares about finding a solution, not necessarily an optimal one.

def BRUTEFORCE(puzzle, goal):
	states = []
	win = False
	counter = 0
	solution = []

	states.append(copy.deepcopy(puzzle))

	while(not win):
		moveList = rules(states[counter])

		for x in range(0, len(moveList)):
			newPuzzle = moveTile(copy.deepcopy(states[len(states)-1]), moveList[x], True)


			if not(newPuzzle in states):
				states.append(newPuzzle)
				counter+=1
				solution.append(moveList[x])
				printPuzzle(states[len(states)-1], 'progress', counter, moveList[x])
			else:
				states.remove(newPuzzle)
				counter-=1


			if newPuzzle == goal:
			 	win = True
			 	printPuzzle(newPuzzle, 'progress', counter)
			 	print "SOLVED"
			 	print "BRUTEFORCE Solution:", solution



# A* algorithm.
# simulates all possible moves, calculates the best moves
# possible via hueristic algorithm. Very optimal solution.

def aStar(puzzle, goal):
	moveCount = 0;

	hLarge = 1000 # temp value for heuristicLarge
	hSmall = -1 
	bestMove = ''
	states = [] # will hold all states we have been to
	moves = [] # will hold all moves we made
	solution = []


	while (puzzle != goal):

		time.sleep(1) # delay's output so you can visualize the algorithm

		moveList = rules(puzzle, bestMove)

		for x in range(0, len(moveList)):
			hSmall = moveTile(puzzle, moveList[x])
		 	if hSmall < hLarge: # if the new heuristic value is smaller than current, replace it
		 		hLarge = hSmall
		 		bestMove = moveList[x] # update best move for smaller heuristic value

		moveTile(puzzle, bestMove, True)

		moveCount +=1
		printPuzzle(puzzle, 'progress', moveCount, bestMove)

		solution.append(bestMove)


		hLarge = 1000 # reinitiate hLarge and hSmall
		hSmall = -1

	print "SOLVED"
	print "A* Solution:", solution


import json
from pprint import pprint
import copy
import time
import random

fileName = '4-moves.json'
with open(fileName) as data_file:
	data = json.load(data_file)

validateMatrix(data) # exits program if invalid matrix was given

printPuzzle(data,'start')
printPuzzle(data,'goal')

puzzle = copy.deepcopy(data['start'])
puzzle2 = copy.deepcopy(data['start'])
puzzle3 = copy.deepcopy(data['start'])

print "\nSolving puzzle via backtracking:"
backtracking(puzzle, data['goal'], int(fileName[0])) # first character of filename indicates number of moves

time.sleep(3)
print "\nSolving puzzle via A* algorithm:"
aStar(puzzle2, data['goal'])


#time.sleep(3)
#print "\nSolving puzzle via BRUTE FORCE"
#BRUTEFORCE(puzzle, data['goal'])

# Still need to implement a menu, can un-comment algorithm choice for now