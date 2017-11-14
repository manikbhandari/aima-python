from gen_packages.generate_packages import create_packages


packages_A = create_packages(1)
packages_B = create_packages(2)
packages_C = create_packages(3)

for row in packages_A:
	print row

print ""
for row in packages_B:
	print row
print ""
for row in packages_C:
	print row
