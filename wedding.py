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

    def __init__(self, init):

        # Parse the input file
        self.object = self.parse_file(init)
        self.initial = self.initSolution(self.object)

    # Returns all differents states obtained by swapping 2 tables
    def successor(self, state):
        pass

    def value(self, state):
        pass

    #read the file, create the list and code it for the state schema
    def parse_file(self,path):

        file_init  = open(path, 'r')
        grid = []
        i = -2

        for line  in file_init:
            if i == -2 :
                    nbr_guests = line
            elif i == -1 :
                    nbr_tables = line
            else :
                #return all value in line, using sep as the delimiter string
                cols = line.split(" ")
                grid.append([])
                for col in cols:
                    if len(col)>0:
                        grid[i].append(int(col))
            i += 1

        file_init.close()

        return int(nbr_guests), int(nbr_tables), grid

    def initSolution(self, object):

        nbr_guests, nbr_tables, grid = object
        #value of the initial solution
        value = 0
        #number of guests in each table
        s = nbr_guests / nbr_tables

        #set of tables
        tables = []
        t = 0

        for i in range(nbr_guests-1):

            #check if person i is already on a table
            if self.isAvailable(i, tables) :
                tables.append([])
                #first unsigned person for a table
                tables[t].append(int(i))

                #fill tables[t]
                value = self.fillTable(i, nbr_guests, s, tables[t], tables, grid, value)
                #Go to the next table
                t += 1
        return value, tables


    #Check person p is already on a table
    def isAvailable(self, p, tables):
        for table in tables :
            for guest in table :
                if guest == p :
                    return False
        return True

    #Fill the table t
    def fillTable(self, p, n, s, table, tables, grid, value):

        #level of affinity [-5;+5]
        aff_level = 5

        #while the table[t] is not full
        while(len(table) < s) :
            for j in range(n):
                #check if person j is already on a table
                if self.isAvailable(j, tables):
                    if grid[p][j] == aff_level:
                        if len(table) < s :
                            table.append(int(j))
                            value += grid[p][j]
            if aff_level == -5 :
                aff_level = 5
            else :
                aff_level -= 1
        #sort the table when is full
        table.sort()
        return value

    #Get value of the solution
    def getValue(self, tables):
        value = 0
        for table in tables :
            value += sum(table)
            print("Value")
            print(value)
        return value



###############
# State class #
###############
# This class represents a state. A state is represented by a matrix.
# At each different state, the matrix  is different too.
# A matrix is an attribute of the class State.
class State:

    def __init__(self, n, t, m, tables, value):
        self.guests = n
        self.tables = t
        self.affinities_matrix = m
        self.tables = tables
        self.value = value


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

    for step in range(limit):
        if callback is not None:
            callback(current)

        best_choices = []
        min_value = 0
        min_node = None

        for node in list(current.expand()):
            if len(best_choices) < 5:
                # If there is less than 5 node in the best_choices,
                # we can add a node without removing another one from best_choices.
                if min_node == None:
                        # If this is the first node to add to best_choice
                        # Initial step
                        best_choices.append(node)
                        min_node = node
                        min_value = node.value()
                else:
                    best_choices.append(node)
                    for best_node in best_choices:
                        if best_node.value() < min_value:
                            # we have to keep track of the current minimum node in case of remove
                            min_value = best_node.value()
                            min_node = best_node
            else:
                if node.value() > min_value:
                    # Delete from best_choices the node containing the lowest value
                    best_choices.remove(min_node)
                    best_choices.append(node)
                    min_value = node.value()
                    min_node = node
                    for best_node in best_choices:
                        # Make sure that we keep track of the correct node
                        # containing the minimum value
                        if best_node.value() < min_value:
                            min_value = best_node.value()
                            min_node = best_node

        current = random.choice(best_choices)

        if current.value() > best.value():
            best = current
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

        # max_value contains the current max value in the neighborhood
        max_value = 0
        # max_node contains the current node containing the current maximum value
        max_node = current

        for node in list(current.expand()):
            if node.value() > max_value:
                max_value = node.value()
                max_node = node

        current = max_node
        if current.value() > best.value():
            best = current
    return best

####################
# Launch the search#
###################

if __name__ == '__main__':
	wedding = Wedding(sys.argv[1])
	print(wedding.initial)

	#node = randomized_maxvalue(wedding, 100)
	# node = maxvalue(wedding, 100)

	#state = node.state
	#print(state)
