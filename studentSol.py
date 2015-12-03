#!/usr/bin/env python3

import rpg

def get_clauses(merchant, level):
		# Append all clauses needed to find the correct equipment in the 'clauses' list.
		#
		# Minisat variables are represented with integers. As such you should use
		# the index attribute of classes Ability and Equipment from the rpg.py module
		# 
		# The equipments and abilities they provide read from the merchant file you passed
		# as argument are contained in the variable 'merchant'.
		# The enemies and abilities they require to be defeated read from the level file you
		# passed as argument are contained in the variable 'level'
		# 
		# For example if you want to add the clauses equ1 or equ2 or ... or equN (i.e. a
		# disjunction of all the equipment pieces the merchant proposes), you should write:
		# 
		# clauses.append(tuple(equ.index for equ in merchant.equipments))
		#
		clauses = []
		#Provided
		for equ1 in merchant.equipments:
			for abi in equ1.provides:
				clauses.append((-equ1.index,abi.index))

		#IsProvided
		for abi in merchant.abilities:
			clauses.append((-abi.index,)+tuple([provided.index for provided in abi.provided_by]))

		#Conflict
		for equ2 in merchant.equipments:
			clauses.append((-equ2.index,-(equ2.conflicts.index)))

		return clauses




def get_nb_vars(merchant, level):
		# nb_vars should be the number of different variables present in your list 'clauses'
		# 
		# For example, if your clauses contain all the equipments proposed by merchant and
		# all the abilities provided by these equipment, you would have:
		#nb_vars = len(merchant.abilities) + len(merchant.equipments)
		diff_vars =[]
		clauses = get_clauses(merchant,level) # Retourne toutes les clauses de la liste 'clauses'
		for clause in clauses:
			for element in clause :
				isIn = False # isIn est mis initialement à False
				for var in diff_vars:
					if var == element:
					    isIn = True
				if not isIn:
					diff_vars.append(element)
		nb_vars = len(diff_vars)
		return nb_vars


