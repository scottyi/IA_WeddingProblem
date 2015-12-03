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





    #Returns all differents states obtained by swapping 2 tables
	def successor(self, state):
         list_size = len(state.list)
         for i in range(list_size):
             for j in range(list_size):
                 if i<j: #avoid identical swaps
                     yield ((i,j),state.swap_city(i,j))



	def value(self, state):
        #TODO
		pass
###############
# State class #
###############

class State:

    def __init__(self, n, t, m, tables, value):
		#TODO
		self.list=[]






    # Swap deux tables
    def swap_tables(self, table1, table2):
        new_state = deepcopy(self)
        tmp = new_state.list[table1]
        new_state.list[table1] = new_state.list[table2]
        new_state.list[table2] = tmp
        return new_state

###########################################
    def __hash__(self):
        s = ""
        for x in range(0, len(self.list)):
            s+=self.list[x]
        return hash(s)


###########################################
    def __eq__(self, state):
        return hash(self) == hash(state)

###########################################
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

# inspiré du code de Ben.D
# Attention: Il faut utiliser seed equal to 42 in your random generator.
def randomized_maxvalue(problem, limit=100, callback=None):
	current = LSNode(problem, problem.initial, 0)
        best = current
        for step in range(limit):
            best_list = []

            for i in list(current.expand()):
                best_list.append([i.value(),i])

            best_list = sorted(best_list, key=lambda b: b[0], reverse=True)

            best_list = best_list[:5]
            tmp = random.choice(best_list)

            current = tmp[1]
            if tmp[0] > best.value():
                best = current
            print(step, -current.value())

        return best

# insipiré du code de Ben.D
def maxvalue(problem, limit=100, callback=None):
	current = LSNode(problem, problem.initial, 0)
        best = current

        for step in range(limit):
            for i in list(current.expand()):
                if i.value() > best.value():
                    best = i
                    best_step = step
            current = best
            print(step, -current.value())
        return best

if __name__ == '__main__':
	wedding = Wedding(sys.argv[1])
	print(wedding.initial)

	node = randomized_maxvalue(wedding, 100)
	# node = maxvalue(wedding, 100)
    # node = random_walk(wedding,100)

	state = node.state
	print(state)
