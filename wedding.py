# coding: utf-8
#!/usr/bin/env python3

'''

NAMES OF THE AUTHOR(S):
Scott IVINZA MBE
Jos ZIGABE
GROUPE 29

'''
################################################################################
#
#		Implementation of the wedding problem class
#
################################################################################

from search import *
from copy import deepcopy
from utils import *
import random
import sys


#################
# Problem class #
#################
class Wedding(Problem):
    # Contains the initial State
	def __init__(self, init_state):
    # Read init matrix and and put it as initial State
           file_init  = open(init_state, 'r')
           i = 0
           j = 0
           matrix = []
           for line in file_init:
                matrix.append([])
                for string in line:
                    for char in string:
                        if char != '\n' and char !='\r':
                            matrix.append(char)
                i+=1
           #self.initial = State(matrix,)
           file_init.close()





    # Returns all differents states obtained by swapping 2 tables
	def successor(self, state):
         list_size = len(state.list)
         for i in range(list_size):
             for j in range(list_size):
                 if i<j: #avoid identical swaps
                     yield ((i,j),state.swap_tables(i,j))


###############
# State class #
###############
# This class represents a state. A state is represented by a matrix.
# At each different state, the matrix  is different too.
# A matrix is an attribute of the class State.
class State:

    def __init__(self, n, t, matrix ):

        self.guests = n # n guests
        self.tables = t # t tables
        self.affinities_matrix = matrix # affinities matrix
        self.height = len(self.affinities_matrix) # height is the number of lines of the affinities matrix
        self.width = len(self.affinities_matrix[0]) # width is  the number of column of the affinities matrix
        self.list = []

    # Swap two tables
    def swap_tables(self, table1, table2):
        new_state = deepcopy(self)
        tmp = new_state.list[table1]
        new_state.list[table1] = new_state.list[table2]
        new_state.list[table2] = tmp
        return new_state

    def __hash__(self):
        s = ""
        for x in range(0, len(self.list)):
            s+=self.list[x]
        return hash(s)


    def __eq__(self, state):
        return hash(self) == hash(state)


    def __str__(self):
        s = ""
        for x in range(0, len(self.list)-1):
            s += str(self.list[x]) + '->'
        s += str(self.list[len(self.list)-1])
        return s

###########################################

################
# Local Search #
################

# randomize maxvalue chooses the next node randomly among  the 5 best neighbors
# (again, even if  it degrades the current solution).
# If callback is not None, it must be a one-argument function that will be
# called at each step with the current node
def randomized_maxvalue(problem, limit=100, callback=None):

	current = LSNode(problem, problem.initial, 0)
        best = current
        random.seed(42) # set the random "seed" to a static value
        for step in range(limit):
            if callback is not None:
                callback(current)
            best_list = []

            for i in list(current.expand()):
                best_list.append([i.value(),i])

            best_list = sorted(best_list, key=lambda b: b[0], reverse=True)

            best_list = best_list[:5]
            tmp = random.choice(best_list) # Chooses the next node randomly among the 5 best neighbors

            current = tmp[1]
            if tmp[0] > best.value():
                best = current
            #print(step, -current.value())

        return best

# maxvalue chooses the best node (i.e., the node with maximum value) in the neighborhood,
# even if it degrades the current  solution.
# If callback is not None, it must be a one-argument function that will be
# called at each step with the current node

def maxvalue(problem, limit=100, callback=None):
	current = LSNode(problem, problem.initial, 0)
        best = current

        for step in range(limit):
            if callback is not None:
                callback(current)

            for i in list(current.expand()):
                if i.value() > best.value():
                    best = i
                    #best_step = step
            #current = best
            #print(step, -current.value())
        return best

####################
# Launch the search#
###################

if __name__ == '__main__':
	wedding = Wedding(sys.argv[1])
	print(wedding.initial)

	node = randomized_maxvalue(wedding, 100)
	# node = maxvalue(wedding, 100)
    # node = random_walk(wedding,100)

	state = node.state
	print(state)
