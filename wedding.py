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
from mimetypes import guess_all_extensions

from search import *
from copy import deepcopy
from utils import *
import random
import sys

matrix = []

#################
# Problem class #
#################
class Wedding(Problem):

    def __init__(self, init):

        # Parse the input file
        guest, tables, grid = self.parse_file(init)
        value, solution = self.initSolution(guest, tables, grid)

        #init the initial state
        self.initial = State(guest, tables, grid, solution, value)

    #Returns all differents states obtained by swapping 2 points in the path."""
    def successor(self, state):

        value, solution = state.getSolution()
        nbr_guests = state.getGuests()
        nbr_tables = state.getTables()
        affinities = state.getAffinities()

        s = nbr_guests / nbr_tables
        i = 0

        for table in solution :
            for p in table :
                #get happiness of p
                happy = self.getHappiness(p, table, affinities)
                if happy != (s-1)*5:
                    new_solution = self.newSolution(p, happy, table, solution, affinities, s)
                    new_value = self.getTotalValue(new_solution, affinities, s)
                    new_state = state.build_state(new_solution, new_value)
                    yield ("swap", new_state)

                i += 1

    def value(self, state):
        value, solution = state.getSolution()
        return value


    def getUnhappy(self, table, affinities, s):
        i = 0

        while(i < s):
            p1 = table[i]
            for p2 in table :
                #if p1 dislike p2, he has to mouve
                if affinities[p1][p2] < 0:
                    return p1
            i += 1
        return None

    def newTable(self, p1, p2, table, s):
        new_table = []
        i = 0
        for p in table :
            new_table.append(p)
            if p == p2 :
                new_table[i] = p1
            i += 1
        new_table.sort()
        return new_table

    #get the level of happiness of p1 in this table
    def getHappiness(self, p1, table, affinities):
        happy = 0
        for p2 in table :
            happy += affinities[p1][p2]

        return  happy



    #swap function
    def swap(self, unhappy1, happiness1, unhappy2, happiness2, t1, t2, cur_solution, s, affinities):

        new_solution = []
        i = 0
        new_table1=[]
        new_table2=[]

        for table in cur_solution :
            if table == t1 :
                for p in table :
                    if p == unhappy1 :
                        if self.getHappiness(unhappy2, table, affinities) > happiness2 :
                            new_table1.append(unhappy2)
                        else :
                            return cur_solution
                    else :
                        new_table1.append(p)
                #sort before
                new_table1.sort()
                if self.getValue(new_table1, affinities, s) > self.getValue(t1, affinities, s) :
                    new_solution.append(new_table1)
            elif table == t2:
                if table == t2 :
                    for p2 in table :
                        if p2 == unhappy2 :
                            if self.getHappiness(unhappy1, table, affinities) > happiness1:
                                new_table2.append(unhappy1)
                            else :
                                return cur_solution
                        else :
                            new_table2.append(p2)
                    #sort before
                    new_table2.sort()
                    new_solution.append(new_table2)

            else :
                new_solution.append(table)


        return new_solution

    #get the new solution
    def newSolution(self, unhappy, happiness, unhappyTable, cur_solution, affinities, s):

        new_solution = []

        for table in cur_solution :
            #Check if we are not in the unhappytable
            if table != unhappyTable :
                for p in table :
                    #get happiness of p
                    happiness2 = self.getHappiness(p, table, affinities)
                    if happiness2 < 0 :
                        #swap to improve happiness
                        new_solution = self.swap(unhappy, happiness, p, happiness2, unhappyTable, table, cur_solution, s, affinities)
        return  new_solution


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

    def initSolution(self, n, t, m):

        nbr_guests = n
        nbr_tables = t
        grid = m

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
                self.fillTable(i, nbr_guests, s, tables[t], tables, grid)

                #sum value of the tables
                value += self.getValue(tables[t], grid, s)
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
    def fillTable(self, p, n, s, table, tables, grid):

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
            if aff_level == -5 :
                aff_level = 5
            else :
                aff_level -= 1
        #sort the table when is full
        table.sort()

    #Get value of the table
    def getValue(self, table, grid, s):
        value = 0
        i = 0

        while (i < s) :
            p1 = table[i]
            for p2 in table :
                value += grid[p1][p2]
            i += 1
        return value

    #Get total value of the solution
    def getTotalValue(self, sol, grid, s):
        total_value = 0

        for table in sol :
            total_value += self.getValue(table,grid,s)

        return total_value



###############
# State class #
###############
# This class represents a state. A state is represented by a matrix.
# At each different state, the matrix  is different too.
# A matrix is an attribute of the class State.
class State:

    def __init__(self, n, t, m, tables, value):
        self.nbr_guests = n
        self.nbr_tables = t
        self.affinities_matrix = m
        self.solution = tables
        self.value = value

    def __str__(self):
        s = ""
        s += str(self.value) + '\n'
        for table in self.solution :
            for p in table :
                s += str(p) + ' '
            s += '\n'
        return s

    def getGuests(self):
        return self.nbr_guests

    def getTables(self):
        return self.nbr_tables

    def getSolution(self):
        return self.value, self.solution

    def getAffinities(self):
        return self.affinities_matrix

    def build_state(self, new_sol, new_val):

        new_state = State(self.nbr_guests, self.nbr_tables, self.affinities_matrix, new_sol, new_val)

        return new_state


################
# Local Search #
################

# randomize maxvalue chooses the next node randomly among  the 5 best neighbors
# (again, even if  it degrades the current solution).
# If callback is not None, it must be a one-argument function that will be
# called at each step with the current node
def randomized_maxvalue(problem, limit=100, callback=None):
    random.seed(42)
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
    print("---- Initial state ----")
    print(wedding.initial)

    #node = random_walk(wedding, 100)
    #node = randomized_maxvalue(wedding, 100)
    node = maxvalue(wedding, 100)

    print("---- Final state ----")
    state = node.state
    print(state)
