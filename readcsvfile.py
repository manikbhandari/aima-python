import csv
import numpy as np

def get_details(filename):
	courses = []
	profs = []
	with open('testcasefile.csv', 'rb') as csvfile:
		filereader = csv.reader(csvfile, delimiter=',')
		table = [row for row in filereader]
		ind = -1
		for i in range(len(table)):
			if table[i][0] == 'Prof-1':
				ind = i
				break
		if ind == -1:
			print "no professor detail was supplied"
		table = np.array(table)
		courses = table[2:ind-2, :]
		profs = table[ind:len(table), :]
		return (courses, profs)

