import sys

#Create the array 'vasp' with all the lines of vasprun.xml file
with open(sys.argv[1],'rb') as vaspfile: 
    vasp = vaspfile.readlines()

#Find last finished step and first line of this step
n = 0
last_step = 0
last_line = 0
for v in vasp:
    if v == ' <calculation>\n':
        last_step += 1

while n < last_step - 1:
    if vasp[last_line] == ' <calculation>\n':
        n += 1
        last_line += 1
    else:
        last_line += 1

#Find the <structure> within the last finished step
k = last_line - 1 
while k < len(vasp):
    if vasp[k] == '  <structure>\n':
        begin_struct = k
        k += 1
    elif vasp[k] == '  </structure>\n':
        end_struct = k
        k += 1
    else:
        k += 1        

#Increase the level of <structure> to an equivalent of <calculation>
for k in range(begin_struct, end_struct + 1):
    line = list(vasp[k])
    del line[0]
    vasp[k] = ''.join(line)    

#Write the result in the vasprun file
#1 Write the first unchanged lines
vaspnew = open("vasprun.xml-new","w+")
for k in range(last_line - 1):
    vaspnew.write(vasp[k])

#1 Write the final structure
vaspnew.write(' <structure name="finalpos" >')

for k in range(begin_struct + 1, end_struct + 1):
    vaspnew.write(vasp[k])

vaspnew.write('</modeling>')
vaspnew.close()
