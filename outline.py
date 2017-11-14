from logic import *
import itertools
from kb_utils import get_clauses
class FolKB(KB):
	def __init__(self, init_clauses = []):
		self.clauses = []
		for clause in init_clauses:
			self.tell(clause)
	def tell(self, sentence):
		self.clauses.append(sentence)
	
	def ask(self, algo, query):
		if algo == 1:
			fol_fc_ask(self, query)

	def retract(self, sentence):
		self.clauses.remove(sentence)

def fol_fc_ask(KB, query):	
	answers = []
		
	while True:	
		newrules = []
		for rule in KB.clauses:
			#print rule,"______________________________"
			#if rule can unify query then you have your answer
			assign = unify(rule, query, {})
			if assign is not None:
				answers.append(assign)
			p,q = get_pq(rule)
			for theta in get_thetas(KB,p):
				p_clauses =  set(flatten(subst(theta,p), '&'))
				
				#If we find a valid substitution 
				if p_clauses.issubset(set(KB.clauses)):
					
					#Consequence with substituted values must also be true
					qnew = subst(theta, q)
					#If this was not already present
					q_already_present = 0
					for clause in KB.clauses:
						if unify(clause, qnew, {}) is not None:
							q_already_present = 1
					for clause in newrules:
						if unify(clause, qnew, {}) is not None:
							q_already_present = 1
					if q_already_present == 0:
						#add it to newrules
						newrules.append(qnew)
					#if qnew answers the query then save this
					assign = unify(qnew, query, {})
					if assign is not None:
						#need to handle multiple solutions
						answers.append(assign)
		#at end of iteration if no new rules are added then break
		if len(newrules) == 0:
			break
		#otherwise add the new rules to the KB
		for clause in newrules:
			KB.tell(clause)
	#return the unique substitutions
	unique = []
	for d in answers:
		if dict_present(d, unique) == 0:
			unique.append(d)
	return unique
	
def get_objects(clause):
	if not clause.args:
		if str(clause)[0].isupper():
			return [clause]
	objects = []
	for arg in clause.args:
			objects += get_objects(arg)
	return set(objects)


def get_variables(clause):
	#return "all the variables in the clause"
	if not isinstance(clause,Expr):
		return
	if is_variable(clause):
		return [clause]
	elif clause.args is None:
		return []
	variables = []
	for arg in clause.args:
		var = get_variables(arg)
		if var is not None:
			variables += var
	return set(variables)

def get_pq(definiteclause):
	if is_symbol(definiteclause.op):
		return [], definiteclause
	else:
		p,q = definiteclause.args
		return p, q

def get_thetas(KB, antecedant):
	variables = get_variables(antecedant)
	if variables is None:
		variables = []
	#get all the constants from the knowledge base
	constants = []
	for clause in KB.clauses:
		for const in get_objects(clause):
			constants.append(const)
	constants = set(constants)
#	print constants	
	thetas = []
	all_possible_assigns = itertools.product(constants, repeat = len(variables))
	for assignments in all_possible_assigns:
		theta = {}
		for var, assign in zip(variables, assignments):
			#print var, assign
			theta[var] = assign
			thetas.append(theta)
	return thetas
	
def flatten(s, op):
	if s.op == op:
		res = []
		for arg in s.args:
			res += flatten(arg, op)
		return res
	else:
		return [s]

def dict_present(d, l):
	if len(l) == 0:
		return 0
	for d_ in l:
		diff = 0
		for key in d:
			if str(d[key]) != str(d_[key]):
				#this d_ is different than d
				diff = 1
		#d exists in l
		if diff == 0:
			return 1
	return 0

def fol_bc_ask(KB, goals, thetas):
	answers = []
	if not goals:
		return thetas
	q_ = compsubst(thetas, goals[0])	
	print q_
	for rule in KB.clauses:
		p,q = get_pq(rule)
		#print type(p)
		#print p
		p_clauses = []
		if isinstance(p,Expr): 
			p_clauses =  set(flatten(p, '&'))
		if unify(q,q_,{}) is not None:
			theta = unify(q,q_,{})
			new_goals = []
			if p_clauses is not None:
				for clause in p_clauses:
					new_goals.append(clause)
			#print new_goals
			for i in range(1, len(goals)):
				new_goals.append(goals[i])
			new_goals = set(new_goals)
			#for goal in new_goals:
			#	print goal
			thetas.append(theta)
			answers += fol_bc_ask(KB,list(new_goals),thetas)
	return answers

def compsubst(thetas, goal):
	p = goal
	if thetas is None or len(thetas) == 0:
		return p
	for theta in thetas:
		p = subst(theta, p)
		#print p
	return p
#__________________________________________________________________________________
#kb1 = FolKB(get_clauses('rulefile1.txt'))
criminalkb = FolKB()
with open('example.txt') as f:
	content = [line.strip("\n") for line in f.readlines()]
for sentence in content:
	criminalkb.tell(expr(sentence))
#cl = criminalkb.clauses[-3]
#print fol_fc_ask(kb1, expr('Alive(Marcus,t)'))
fol_bc_ask(criminalkb,[expr('Criminal(West)')],[])

