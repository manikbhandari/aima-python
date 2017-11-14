#Basic state class
class State:
	def __init__(self):
		self.state = [[0 for i in range(4)] for j in range(4)]
	#returns a list of colums that the next coin can be placed in
	#Complexity - O(16)
	def actions(self):
		st = self.state
		ac = []
		for c in range(4):
			for r in range(4):
				if st[r][c] == 0:
					ac.append(c)
					break
		return ac
	#returns 1 if p1 wins, -1 if p2 wins, 0 if draw and 2 if it is not a terminal state
	def terminalTest(self):
		st = self.state
		#check if any 3 1's or -1's are alligned in a row
		for r in range(4):
			for c in range(2):
				if (st[r][c] == 1 and st[r][c+1] == 1 and st[r][c+2] == 1) :
					return 1
				elif (st[r][c] == -1 and st[r][c+1] == -1 and st[r][c+2] == -1):
					return -1
		#check if any 3 1's or -1's are alligned in a column
		for c in range(4):
			for r in range(2):
				if (st[r][c] == 1 and st[r+1][c] == 1 and st[r+2][c] == 1):
					return 1
				elif (st[r][c] == -1 and st[r+1][c] == -1 and st[r+2][c] == -1):
					return -1
		#check for 3 1's or -1's along the main diagonal
		for r in range(2,4):
			for c in range(2, 4):
				if (st[r][c] == 1 and st[r-1][c-1] == 1 and st[r-2][c-2] == 1) :
					return 1
				elif (st[r][c] == -1 and st[r-1][c-1] == -1 and st[r-2][c-2] == -1):
					return -1
		#check for 3 1's or -1's along alternate diagonal
		for r in range(2,4):
			for c in range(0,2):
				if (st[r][c] == 1 and st[r-1][c+1] == 1 and st[r-2][c+2] == 1):
					return 1
				elif (st[r][c] == -1 and st[r-1][c+1] == -1 and st[r-2][c+2] == -1):
					return -1
		#check for draw i.e. all moves have been played
		draw = 1
		for r in range(4):
			for c in range(4):
				if st[r][c] == 0:
					draw = 0
		if draw == 1:
			return 0

		return 2

	def utility(self):
		ans = self.terminalTest()
		if ans == 2:
			print "This is not a terminal state"
		return ans

	def result(self, action, minormax):
		st = self.state
		ns = State()
		#ns.state = st
		for r in range(4):
			for c in range(4):
				ns.state[r][c] = st[r][c]
		for r in range(4):
			if ns.state[r][action] == 0:
				ns.state[r][action] = minormax
				break
		return ns

#s = State()
#print s.state
#print s.actions()
#print s.terminalTest()
# print s.result(3, 1).state

T = {}
neginf = -10
posinf = 10
#input is a state an it returns an action
def alphaBetaPruning(s):
	# print s.state
	v = maxVal(s, neginf, posinf)
	# print "v = " + str(v)
	# print "actions are: ", s.actions()
	# print s.state

	for c in s.actions():
		ns = s.result(c, 1)
		ind = hashFunc(ns)
		# print "to find: ", ind
		if ind in T:
			if T[ind] == v:
				return c
	print "Some problem occured in alpha beta pruning"
	return -1
def maxVal(s, alpha, beta):
	ind = hashFunc(s)
	tt = s.terminalTest()
	if tt == -1 or tt == 1 or tt == 0:
		T[ind] = s.utility()
		return T[ind]
	v = neginf
	for a in s.actions():
		ns = s.result(a,1)
		v = max(v, minVal(ns, alpha, beta))
		if v >= beta:
			return v
		alpha = max(alpha, v)
	T[ind] = v
	return v

def minVal(s, alpha, beta):
	ind = hashFunc(s)
	tt = s.terminalTest()
	if tt == -1 or tt == 1 or tt == 0:
		T[ind] = s.utility()
		return T[ind]
	v = posinf
	for a in s.actions():
		ns = s.result(a, -1)
		v = min(v, maxVal(ns, alpha, beta))
		if v <= alpha:
			return v
		beta = min(beta, v)
	T[ind] = v
	return v
def hashFunc(s):
	st = s.state
	l = []
	for r in range(4):
		for c in range(4):
			l.append(st[r][c])
	t = tuple(l)
	return t


s1 = State()
s1.state = [[1, -1, 1, -1], [1, -1, 1, -1], [-1, 0, 0, 1], [-1, 0, -1, 0]]
print alphaBetaPruning(s1)
# for state in T:
# 	print state, T[state]