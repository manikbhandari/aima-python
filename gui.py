import Tkinter
import turtle
import numpy as np
import random

def run_turtles(*args):
    for t, d in args:
        t.circle(250, d)
    root.after_idle(run_turtles, *args)

def generateEnv(r, c, p):
    env = np.zeros((r,c))
    indexes = random.sample(np.arange(0, r*c), int(float(p)/100*r*c))
    for num in indexes:
        env[num/r, num%c] = 1
    return env

root = Tkinter.Tk()
root.withdraw()

env = generateEnv(10,10,30)
col = ['yellow', 'brown']

frame = Tkinter.Frame(bg='black')
# Tkinter.Label(frame, text=u'Hello', bg='grey', fg='white').pack(fill='x')

for r in range(10):
    for c in range(10):
        Tkinter.Label(frame, bg=col[int(env[r,c])], width=5).pack()

canvas = Tkinter.Canvas(frame, width=750, height=750)
canvas.pack()
frame.pack(fill='both', expand=True)

turtle1 = turtle.RawTurtle(canvas)
turtle2 = turtle.RawTurtle(canvas)

turtle1.ht(); turtle1.pu()
turtle1.left(90); turtle1.fd(250); turtle1.lt(90)
turtle1.st(); turtle1.pd()

turtle2.ht(); turtle2.pu()
turtle2.fd(250); turtle2.lt(90)
turtle2.st(); turtle2.pd()

root.deiconify()	

run_turtles((turtle1, 3), (turtle2, 4))

root.mainloop()