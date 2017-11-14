#Constraints to keep in mind
#All courses in a package must be connected because no clash
#There must be 2 lab sections for each lab
#All lab sections in the afternoon and must be continuous
#Tutorial cannot be held in the same day as lecture so Course_L and Course_T will be connected
#No 2 dc in succession so all dcs of a program will be connected
#Not all ge on the same day so all ge will be connected
#At most 1 lecture secion of a course in a day so all Course_L will be connected
#Domains of professor 4 and professor 1 need to be modified
#No course of a prof in succession and also no clash so all courses by same prof will be connected

import numpy as np
from gen_packages.generate_packages import create_packages
from gen_packages.readcsvfile import get_details

courses, profs = get_details('testcasefile.csv')

def flatten_packages(program):
	packages = create_packages(program)
	flat_packages = []
	for package in packages:
		flat_list = []
		for sublist in package:
			for item in sublist:
				flat_list.append(item)
		flat_packages.append(flat_list)
	return flat_packages

def make_unique(cg):
	for course in cg:
		cg[course] = list(set(cg[course]))
def get_ltp(course):
	ltp = courses[course][4]
	splitted = ltp.split()
	l = int(splitted[0])
	t = int(splitted[1])
	p = int(splitted[2])
	return l, t, p
	
def get_courses(program):
	allcourses = {}
	for i in range(len(courses)):
		if courses[i][program] != 'NA':
			l, t, p = get_ltp(i)
			allcourses[courses[i][0]] = []
			for j in range(1, l+1):
				allcourses[courses[i][0]].append(courses[i][0]+"_L" + str(j))
			for j in range(1, p+1):
				allcourses[courses[i][0]].append(courses[i][0]+"_P" + str(j))
			for j in range(1, t+1):
				allcourses[courses[i][0]].append(courses[i][0]+"_T" + str(j))
	return allcourses

def add_package_constraint(cg, program):
	allcourses = get_courses(program)
	packages = flatten_packages(program)
	for package in packages:
		for c1 in package:
			for c2 in package:
				if c1 == c2:
					continue
				for item in allcourses[c1]:
					if item not in cg:
						cg[item] = []
					cg[item] += allcourses[c2]
				for item in allcourses[c2]:
					if item not in cg:
						cg[item] = []
					cg[item] += allcourses[c1]
	make_unique(cg)		


def add_tutorial_constraint(cg, program):
	allcourses = get_courses(program)
	for i in range(len(courses)):
		if courses[i][program] == 'NA':
			continue

		l, t, p = get_ltp(i)	
		if t > 0:
			for lec in range(l):
				tut = courses[i][0] + "_T" + str(1)
				lecture = allcourses[courses[i][0]][lec]

				if lecture not in cg:
					cg[lecture] = []
				cg[lecture].append(tut)
				
				if tut not in cg:
					cg[tut] = []
				cg[tut].append(lecture)
				
	make_unique(cg)

def add_ge_constraint(cg, program):
	from gen_packages.generate_packages import get_course_categories
	allcourses = get_courses(program)
	dc, de, ge = get_course_categories(program)
	for c1 in ge:
		for c2 in ge:
			if c1 == c2:
				continue
			for item in allcourses[c1]:
				#print c1, c2, item
				if item not in cg:
					cg[item] = []
				cg[item] += allcourses[c2]
				#print len(cg[item])
			for item in allcourses[c2]:
				if item not in cg:
					cg[item] = []
				cg[item] += allcourses[c1]
	make_unique(cg)		

def add_lecture_constraint(cg, program):
	allcourses = get_courses(program)	
	for i in range(len(courses)):
		if courses[i][program] == 'NA':
			continue
		l, t, p = get_ltp(i)
		if l > 0:
			for l1 in range(l):
				for l2 in range(l):
					if l1 == l2:
						continue
					lect1 = allcourses[courses[i][0]][l1]
					lect2 = allcourses[courses[i][0]][l2]
					if lect1 not in cg:
						cg[lect1] = []
					if lect2 not in cg:
						cg[lect2] = []
					cg[lect1].append(lect2)
					cg[lect2].append(lect1)
	make_unique(cg)

def add_prof_constraint(cg):
	import re
	allc1 = get_courses(1)
	allc2 = get_courses(2)
	allc3 = get_courses(3)		
	allc1.update(allc2)
	allc1.update(allc3)
	allcourses = allc1
	for row in profs:
		courses_taught = []
		for c in row:
			if re.match("C", c):
				courses_taught.append(c)
			for c1 in courses_taught:
				for c2 in courses_taught:
					if c1 == c2:
						continue
					for item in allcourses[c1]:
						if item not in cg:
							cg[item] = []
						cg[item] += allcourses[c2]
					for item in allcourses[c2]:
						if item not in cg:
							cg[item] = []
						cg[item] += allcourses[c1]
	make_unique(cg)		
			
def add_lab_constraint(cg):
	allc1 = get_courses(1)
	allc2 = get_courses(2)
	allc3 = get_courses(3)		
	allc1.update(allc2)
	allc1.update(allc3)
	allcourses = allc1
	for i in range(len(courses)):
		l, t, p = get_ltp(i)
		if p > 0:
			allc = allcourses[courses[i][0]]
			for i in range(len(allc)-p, len(allc)):
				for j in range(len(allc)-p, len(allc)):
					if i == j:
						continue
					if allc[i] not in cg:
						cg[allc[i]] = []
					if allc[j] not in cg:
						cg[allc[j]] = []
					cg[allc[i]].append(allc[j])
					cg[allc[j]].append(allc[i])
	make_unique(cg)

cg = {}
add_package_constraint(cg, 1)
add_package_constraint(cg, 2)
add_package_constraint(cg, 3)
add_tutorial_constraint(cg, 1)
add_tutorial_constraint(cg, 2)
add_tutorial_constraint(cg, 3)
add_ge_constraint(cg, 1)
add_ge_constraint(cg, 2)
add_ge_constraint(cg, 3)
add_lecture_constraint(cg, 1)
add_lecture_constraint(cg, 2)
add_lecture_constraint(cg, 3)
add_prof_constraint(cg)
add_lab_constraint(cg)

for x in sorted(cg['C_11_L1']):
	print x
