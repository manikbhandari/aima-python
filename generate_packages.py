from readcsvfile import get_details
courses, packages = get_details('testcasefile.csv')

#program = 1 means Program A , 2 means Program B and so on
def get_course_categories(program):
	dc = []
	de = []
	ge = []
	for course in range(len(courses)):
		if courses[course][program] == 'DC':
			dc.append(courses[course][0])

		if courses[course][program] == 'DE':
			de.append(courses[course][0])
		
		if courses[course][program] == 'GE':
			ge.append(courses[course][0])

	return dc, de, ge

#there is a better way to write this.
def create_packages(program):
	packages = []
	dc, de, ge = get_course_categories(program)
	for dc1 in range(0, len(dc)):
		for dc2 in range(dc1+1, len(dc)):
			for dc3 in range(dc2+1, len(dc)):
				for de1 in range(0, len(de)):
					for de2 in range(de1+1, len(de)):
						for ge1 in range(0, len(ge)):
							packages.append([[dc[dc1], dc[dc2], dc[dc3]], [de[de1], de[de2]], [ge[ge1]]])
	return packages
