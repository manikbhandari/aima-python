from logic import *
import re

def for_all_elimination(s):
	return re.sub('For_every [a-z]* ', '', s)

def find_fact(s, pat):
	
	pat = r'(\w*\(%s\)\w*)' % pat      
	return re.findall(pat, s)

def there_exists_elimination(s):
	#search for word after There_exists
	added_const = []
	d = re.findall(r'(?<=There_exists )\w+', s)
	if d:
		for m in d:
			#substitute word in string with uppercase
			repl = "\\b" + m + "\\b"
			s = re.sub(repl, m.upper(), s)
			
			M = m.upper()
			added_const.append(M)
	#remove there exists
	return re.sub('There_exists [A-Z]* ', '', s), added_const

def uppercase(matchobject):
	l = matchobject.group(0).split()
	return l[1].upper()
def get_clause_from_const(s, const):
	clauses = []
	#get antecedant
	s_ = s[0:s.find('=')]
	#print s_
	#split in words
	words = s_.split()
	for w in words:
		#print w
		for c in const:
			if c in w:
				clauses.append(w)
	return clauses

def get_clauses(filename):	
	clauses = []
	with open(filename) as rulefile:
		for line in rulefile:
			line = for_all_elimination(line) 
			line, const =  there_exists_elimination(line)
			#print const
			clauses.append(expr(line))
			for clause in get_clause_from_const(line, const):
				#print clause
				if clause is not None:
					clauses.append(expr(clause))
	return clauses

get_clauses('rulefile1.txt')
