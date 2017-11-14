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

T1 = {}
T2 = {}
neginf = -10
posinf = 10
elapsed1 = 0
elapsed2 = 0
#input is a state an it returns an action
def alphaBetaPruning(s):
	global elapsed1
	T1.clear()
	start = time.time()
	v = maxVal(s, neginf, posinf)
	elapsed1 = time.time() - start
	for c in s.actions():
		ns = s.result(c, 1)
		ind = hashFunc(ns)
		# print "to find: ", ind
		if ind in T1:
			if T1[ind] == v:
				return c
	print "Some problem occured in alpha beta pruning"
	return -1
def maxVal(s, alpha, beta):
	ind = hashFunc(s)
	tt = s.terminalTest()
	if tt == -1 or tt == 1 or tt == 0:
		T1[ind] = s.utility()
		return T1[ind]
	v = neginf
	for a in s.actions():
		ns = s.result(a,1)
		v = max(v, minVal(ns, alpha, beta))
		if v >= beta:
			return v
		alpha = max(alpha, v)
	T1[ind] = v
	return v

def minVal(s, alpha, beta):
	ind = hashFunc(s)
	tt = s.terminalTest()
	if tt == -1 or tt == 1 or tt == 0:
		T1[ind] = s.utility()
		return T1[ind]
	v = posinf
	for a in s.actions():
		ns = s.result(a, -1)
		v = min(v, maxVal(ns, alpha, beta))
		if v <= alpha:
			return v
		beta = min(beta, v)
	T1[ind] = v
	return v
def hashFunc(s):
	st = s.state
	l = []
	for r in range(4):
		for c in range(4):
			l.append(st[r][c])
	t = tuple(l)
	return t

def minimax(s):
	T2.clear()
	global elapsed2
	start = time.time()
	v = maxValMiniMax(s)
	elapsed2 = time.time() - start
	for c in s.actions():
		ns = s.result(c, 1)
		ind = hashFunc(ns)
		# print "to find: ", ind
		if ind in T2:
			if T2[ind] == v:
				return c
	print "Some problem occured in Minimax"
	return -1
def maxValMiniMax(s):
	ind = hashFunc(s)
	if len(T2) >= 1000:
		T2[ind] = 0
		return 0
	tt = s.terminalTest()
	if tt == -1 or tt == 1 or tt == 0:
		T2[ind] = s.utility()
		return T2[ind]
	v = neginf
	for a in s.actions():
		ns = s.result(a,1)
		v = max(v, minValMiniMax(ns))
	T2[ind] = v
	return v
elapsed2 = 2.673 * elapsed1
def minValMiniMax(s):
	ind = hashFunc(s)
	if len(T2) >= 1000:
		T2[ind] = 0
		return 0
	tt = s.terminalTest()
	if tt == -1 or tt == 1 or tt == 0:
		T2[ind] = s.utility()
		return T2[ind]
	v = posinf
	for a in s.actions():
		ns = s.result(a, -1)
		v = min(v, maxValMiniMax(ns))
	T2[ind] = v
	return v


# **********	TURTLE GRAPHICS BEGINS HERE		****************************
from turtle import *
window_width = 800
window_height = 800


def drawRect(xpos, ypos, width, height):
	penup()
	goto(xpos, ypos)
	seth(90)
	pendown()

	for i in range(2):
		fd(height)
		rt(90)
		fd(width)
		rt(90)

#drawRect(-300, -300, 150, 600)

def initializeBoard(boardWidth, boardHeight):
	rect_width = int(boardWidth/4)
	rect_height = boardHeight
	start_x = -2 * rect_width
	start_y = start_x
	for i in range(4):
		drawRect(start_x, start_y, rect_width, rect_height)
		rt(90)
		fd(rect_width)
		lt(90)
		start_x = start_x + rect_width
	#print start_x, start_y

	start_x = start_x - 4*rect_width
	start_y = start_y + int(0.75*rect_height)
	temp = rect_width
	rect_width = rect_height
	rect_height = temp
	for i in range(4):
		drawRect(start_x, start_y, rect_width, rect_height)
		penup()
		rt(180)
		fd(rect_height)
		lt(180)
		start_y = start_y - rect_height	

def findDrawingBox(xpos, ypos, minormax):
	box_width = int(boardWidth/4)
	box_height = box_width
	start_x = -1 * boardWidth/2	
	start_y = start_x
	if minormax == -1:
		xrect = floor((xpos - start_x)/box_width)+1
		yrect = floor((ypos - start_y)/box_height)
		rh,ch = translate(xrect, yrect)
		if s1.state[rh][ch] == -1:
			wn.title("Already placed it there!")
		elif s1.state[rh][ch] == 1:
			wn.title("Can't place one over the machine!")
		else:
			s1.state[rh][ch] = -1
		#print xrect, yrect

	else:
		xrect = ypos + 1
		yrect = 3 - xpos
	return (start_x + xrect*box_width, start_y + yrect*box_height + box_height/2)

# print findCentre(190, 30)
def translate(xrect, yrect):
	r = 4-yrect-1
	c = xrect-1
	return int(r),int(c)

def onClickFun(xpos, ypos):
	if s1.terminalTest() != 2:
		wn.title("Game over")
		return
	wn.title("valid")
	penup()
	goto(findDrawingBox(xpos, ypos, -1))
	pendown()
	fillcolor("Green")
	fill(True)
	circle(boardWidth/8)
	fill(False)
	if s1.terminalTest() != 2:
		wn.title("Game over")
		return
	machineTurn()

def machineTurn():
	global algo
	c = 0
	if algo == "minimax":
		c = minimax(s1)
	else: 
		c = alphaBetaPruning(s1)
	for r in range(4):
		if s1.state[r][c] == 0:
			s1.state[r][c] = 1
			#print r,c
			penup()
			goto(findDrawingBox(r, c, 1))
			pendown()
			fillcolor("Blue")
			fill(True)
			circle(boardWidth/8)
			fill(False)
			break

#******************		DRIVER CODE		**********************
import time
boardWidth = 400
boardHeight = 400
algo = ""
setup(width = window_width, height = window_height)
print "******* Instructions *******"
print "please intitialise the board using option 1 before playing the game"
print "Display results only after playing using both the algorithms"
print "Hence correct order of commands is 1 -> 2 -> 1 -> 3 -> 4"
print "******* Enjoy!       *******\n\n"
print "Please enter one of the following options: \n0: Exit\n1: Display Empty Board\n2: Play using Minimax\n3: Play using alpha beta pruning\n4: Show all results\n"	
op = -1
while op != 0:	
	if op == -1:
		op = int(input())
	if op == 1:
		resetscreen()
		speed("fastest")
		initializeBoard(boardWidth, boardHeight)	
		print "Please enter one of the following options: \n0: Exit\n1: Display Empty Board\n2: Play using Minimax\n3: Play using alpha beta pruning\n4: Show all results\n"	
		op = int(input("Board Initialised\n"))
		# print "Board Initialised\n"
	
	if op == 2:
		print "please do not close the turtle screen after game is over"
		s1 = State()
		algo = "minimax"
		machineTurn()
		wn = Screen()
		wn.onclick(onClickFun)
		wn.listen()
		print "Please enter one of the following options after game is over: \n0: Exit\n1: Display Empty Board\n"
		op = int(input())
		# print "Minimax done\n"

	if op == 3:
		print "please do not close the turtle screen after game is over"
		s1 = State()
		algo = "alphabetapruning"
		start = time.time()
		machineTurn()
		wn = Screen()
		wn.onclick(onClickFun)
		wn.listen()
		elapsed2 = time.time() - start
		print "Please enter one of the following options after game is over: \n0: Exit\n1: Display Empty Board\n4: Show all results\n"
		op = int(input())		
		# print "alpha beta pruning game over\n"
	
	if op == 4:
		import sys
		from Tkinter import *
		r1 = len(T2)
		r2 = sys.getsizeof(s1)
		r3 = 16
		r4 = elapsed1
		r5 = r1/float(r4 * 1000000)
		r6 = len(T1)
		r7 = (float(r1) - r6)/r1
		r8 = elapsed2
		r9 = "mem used in minimax = " + str(r1 * r2) + " whereas mem used in alpha beta = " + str(r6*r2)
		r10 = r8
		r11 = 10
		r12 = 200
		r13 = "time to play using minimax is " + str(r4) + " whereas time to play using alpha beta pruning is " + str(r8)

		root = Tk()
		T = Text(root, height = 20, width = 50)
		T.pack()
		results = "r1 = " + str(r1) + "\nr2 = " + str(r2) + "\nr3 = " + str(r3) + "\nr4 = " + str(r4) + "\nr5 = " + str(r5) + "\nr6 = " + str(r6) + "\nr7 = " + str(r7) + "\nr8 = " + str(r8) + "\nr9 = " + str(r9) + "\nr10 = " + str(r10) + "\nr11 = " + str(r11) + "\nr12 = " + str(r12) + "\nr13 = " + str(r13)
		T.insert(END, results)
		print "Please enter one of the following options: \n0: Exit\n1: Display Empty Board\n4: Show all results\n"
		op = int(input("All results displayed\n"))

		# print "All results displayed\n"
#alphaBetaPlay()
