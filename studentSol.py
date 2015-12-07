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
		clauses = []
		clauses.append(tuple(equ.index for equ in merchant.equipments))

		for ability_name in level.ability_names:
			for merchant_ability in merchant.abilities:
				if ability_name == merchant_ability.name:
					isProvided =[]
					isProvided.append(-merchant_ability.index)

					clauses.append([merchant_ability.index])

					for equipment in merchant_ability.provided_by:
						isProvided.append(equipment.index)

					clauses.append(isProvided)

		for equipment in merchant.equipments:
			conflicts = [-equipment.index]

			for ability in equipment.provides:
				clauses.append([-equipment.index,ability.index])
			conflicts.append(-equipment.conflicts.index)
			clauses.append(conflicts)


		return clauses




def get_nb_vars(merchant, level):
		# nb_vars should be the number of different variables present in your list 'clauses'
		# 
		# For example, if your clauses contain all the equipments proposed by merchant and
		# all the abilities provided by these equipment, you would have:
		nb_vars = len(merchant.abilities) + len(merchant.equipments)

		return nb_vars


