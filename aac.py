#/~aac.py
"""
MIT License

Copyright (c) 2022 thepiger4009

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from linecache import getline

#Variables
lc = 1
vb = 0

last_address_given = 0

#Variable Arrays
variableNameList = [0] * 10000
variableAddressList = [0] * 10000
variableCounter = 0

#Address/Label Arrays
labelNameList = [0] * 10000
labelAddressList = [0] * 10000
labelCounter = 0

#Files
rom = open("rom.txt","w+")
debug = open("aac_debug.txt","w+")

#Functions
def getVariableAddress(name):
	for x in range(10000):
		if name == variableNameList[x]:
			break
	return variableAddressList[x]

def getLabelAddress(name):
	for x in range(10000):
		if name == labelNameList[x]:
			break
	return labelAddressList[x]

# Lets check for any address sets!
while 1:
	line = getline("asm.txt",lc).rstrip("\n")
	fullLine = line.split()

	if fullLine[0] == ".var": # Create a variable label at specified address
		name = fullLine[1] # NAME
		address = fullLine[2] # Address
		variableNameList[variableCounter] = name
		variableAddressList[variableCounter] = address
		variableCounter+=1


	if fullLine[0] == "*=": # Create a address point or label point
		aon = fullLine[1] # ADDRESS OR NAME
		debug.write("[DEBUG]:")
		if "!" in aon:    # IF IS NAME DO THIS
			try:
				name = aon.split("!"[0])
			except:
				next
			if last_address_given == 0: # IF THERE HAS BEEN NO ADDRESS POINT MAKE ONE AT 256
				last_address_given = 256
			
			# Now lets figure out how far we are from the last address
			distance = int(last_address_given) + int(vb)

			# Now lets create the label
			labelNameList[labelCounter] = name[1]
			labelAddressList[labelCounter] = distance
			labelCounter+=1

			print("[aac]: Label Created:",name[1],"located at",distance)
			print("[aac]: When calling",name[1],"the returned value is:",getLabelAddress(name[1]))



		else: # IF IS NUMBER DO THIS
			last_address_given = aon
			rom.write("loadAddress\n"),rom.write(aon),rom.write("\n")

	if fullLine[0] == "mov":
		vb+=3

	if fullLine[0] == "jmp":
		vb+=2

	if fullLine[0] == "inc":
		vb+=2

	if fullLine[0] == "dec":
		vb+=2

	if fullLine[0] == "den":
		vb+=1

	if fullLine[0] == "dbk":
		vb+=1

	if fullLine[0] == "sef":
		vb+=2

	if fullLine[0] == "nop":
		vb+=1

	if fullLine[0] == "isp":
		vb+=1

	if fullLine[0] == "dsp":
		vb+=1

	if fullLine[0] == "ehi":
		vb+=1


	lc+=1
	if line == "return 0":
		break
#-------------------------------



#Lets do some instruction assembling!
lc = 1
while 1:
	line = getline("asm.txt",lc).rstrip("\n")
	fullLine = line.split()

	#Lets split this
	try:
		statements = fullLine[1].split(","[0])
	except:
		next

	if fullLine[0] == "mov":
		statement1 = statements[0]
		statement2 = statements[1]


		#----------------------REGISTER X ON SECOND * MOV ?,X * -------------------
		if statement2 == "x": #Doing something to rx
			if "#" in statement1: #Transfering value to it
				try:
					statement3 = statement1.split("#"[0])
				except:
					next
				rom.write("100\n1\n"),rom.write(statement3[1]),rom.write("\n")
			if "$" in statement1: #Transfer memory to it
				try:
					statement3 = statement1.split("$"[0])
				except:
					next
				rom.write("101\n1\n").rom.write(statement3[1]),rom.write("\n")
			match statement1: #Transfer register to register
				case "x":
					rom.write("109\n1\n1\n")
				case "y":
					rom.write("109\n2\n1\n")
				case "t":
					rom.write("109\n3\n1\n")
				case "p":
					rom.write("109\n4\n1\n")
				case "u":
					rom.write("109\n5\n1\n")
			if "!" in statement1: #Transfer variable into register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("101\n1\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement1: #Transfer mem+rp to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("102\n1\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement1: #Transfer mem+ru to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("103\n1\n"),rom.write(statement3[1]),rom.write("\n")
			if statement1 == "stack":
				rom.write("118\n1\n")
		#----------------------REGISTER X ON SECOND * MOV ?,X * -------------------

		#----------------------REGISTER X ON FIRST * MOV X,? * -------------------
		if statement1 == "x": #Doing something to rx
			if "$" in statement2: #Transfer memory to it
				try:
					statement3 = statement2.split("$"[0])
				except:
					next
				rom.write("104\n1\n").rom.write(statement3[1]),rom.write("\n")
			match statement2: #Transfer register to register
				case "x":
					rom.write("109\n1\n1\n")
				case "y":
					rom.write("109\n1\n2\n")
				case "t":
					rom.write("109\n1\n3\n")
				case "p":
					rom.write("109\n1\n4\n")
				case "u":
					rom.write("109\n1\n5\n")
			if "!" in statement2: #Transfer variable into register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("104\n1\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement2: #Transfer mem+rp to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("105\n1\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement2: #Transfer mem+ru to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("106\n1\n"),rom.write(statement3[1]),rom.write("\n")
			if statement2 == "stack":
				rom.write("117\n1\n")
		#----------------------REGISTER X ON SECOND * MOV ?,X * -------------------

		#
		#
		#
		#
		#
		##----------------------REGISTER Y ON SECOND * MOV ?,Y * -------------------
		if statement2 == "y": #Doing something to rx
			if "#" in statement1: #Transfering value to it
				try:
					statement3 = statement1.split("#"[0])
				except:
					next
				rom.write("100\n2\n"),rom.write(statement3[1]),rom.write("\n")
			if "$" in statement1: #Transfer memory to it
				try:
					statement3 = statement1.split("$"[0])
				except:
					next
				rom.write("101\n2\n").rom.write(statement3[1]),rom.write("\n")
			match statement1: #Transfer register to register
				case "x":
					rom.write("109\n1\n2\n")
				case "y":
					rom.write("109\n2\n2\n")
				case "t":
					rom.write("109\n3\n2\n")
				case "p":
					rom.write("109\n4\n2\n")
				case "u":
					rom.write("109\n5\n2\n")
			if "!" in statement1: #Transfer variable into register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("101\n2\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement1: #Transfer mem+rp to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("102\n2\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement1: #Transfer mem+ru to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("103\n2\n"),rom.write(statement3[1]),rom.write("\n")
			if statement1 == "stack":
				rom.write("118\n2\n")
		#----------------------REGISTER Y ON SECOND * MOV ?,Y * -------------------

		#----------------------REGISTER Y ON FIRST * MOV Y,? * -------------------
		if statement1 == "y": #Doing something to rx
			if "$" in statement2: #Transfer memory to it
				try:
					statement3 = statement2.split("$"[0])
				except:
					next
				rom.write("104\n2\n").rom.write(statement3[1]),rom.write("\n")
			match statement2: #Transfer register to register
				case "x":
					rom.write("109\n2\n1\n")
				case "y":
					rom.write("109\n2\n2\n")
				case "t":
					rom.write("109\n2\n3\n")
				case "p":
					rom.write("109\n2\n4\n")
				case "u":
					rom.write("109\n2\n5\n")
			if "!" in statement2: #Transfer variable into register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("104\n2\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement2: #Transfer mem+rp to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("105\n2\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement2: #Transfer mem+ru to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("106\n2\n"),rom.write(statement3[1]),rom.write("\n")
			if statement2 == "stack":
				rom.write("117\n2\n")
		#----------------------REGISTER Y ON SECOND * MOV ?,Y * -------------------
		#
		#
		#
		#
		#
		#
		#
		#----------------------REGISTER T ON SECOND * MOV ?,T * -------------------
		if statement2 == "t": #Doing something to rx
			if "#" in statement1: #Transfering value to it
				try:
					statement3 = statement1.split("#"[0])
				except:
					next
				rom.write("100\n3\n"),rom.write(statement3[1]),rom.write("\n")
			if "$" in statement1: #Transfer memory to it
				try:
					statement3 = statement1.split("$"[0])
				except:
					next
				rom.write("101\n3\n").rom.write(statement3[1]),rom.write("\n")
			match statement1: #Transfer register to register
				case "x":
					rom.write("109\n1\n3\n")
				case "y":
					rom.write("109\n2\n3\n")
				case "t":
					rom.write("109\n3\n3\n")
				case "p":
					rom.write("109\n4\n3\n")
				case "u":
					rom.write("109\n5\n3\n")
			if "!" in statement1: #Transfer variable into register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("101\n3\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement1: #Transfer mem+rp to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("102\n3\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement1: #Transfer mem+ru to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("103\n3\n"),rom.write(statement3[1]),rom.write("\n")
			if statement1 == "stack":
				rom.write("118\n3\n")
		#----------------------REGISTER T ON SECOND * MOV ?,T * -------------------

		#----------------------REGISTER T ON FIRST * MOV T,? * -------------------
		if statement1 == "t": #Doing something to rx
			if "$" in statement2: #Transfer memory to it
				try:
					statement3 = statement2.split("$"[0])
				except:
					next
				rom.write("104\n3\n").rom.write(statement3[1]),rom.write("\n")
			match statement2: #Transfer register to register
				case "x":
					rom.write("109\n3\n1\n")
				case "y":
					rom.write("109\n3\n2\n")
				case "t":
					rom.write("109\n3\n3\n")
				case "p":
					rom.write("109\n3\n4\n")
				case "u":
					rom.write("109\n3\n5\n")
			if "!" in statement2: #Transfer variable into register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("104\n3\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement2: #Transfer mem+rp to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("105\n3\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement2: #Transfer mem+ru to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("106\n3\n"),rom.write(statement3[1]),rom.write("\n")
			if statement2 == "stack":
				rom.write("117\n3\n")
		#----------------------REGISTER T ON SECOND * MOV ?,T * -------------------
		#
		#
		#
		#
		#
		#
		#
		#----------------------REGISTER P ON SECOND * MOV ?,P * -------------------
		if statement2 == "p": #Doing something to rx
			if "#" in statement1: #Transfering value to it
				try:
					statement3 = statement1.split("#"[0])
				except:
					next
				rom.write("100\n4\n"),rom.write(statement3[1]),rom.write("\n")
			if "$" in statement1: #Transfer memory to it
				try:
					statement3 = statement1.split("$"[0])
				except:
					next
				rom.write("101\n4\n").rom.write(statement3[1]),rom.write("\n")
			match statement1: #Transfer register to register
				case "x":
					rom.write("109\n1\n4\n")
				case "y":
					rom.write("109\n2\n4\n")
				case "t":
					rom.write("109\n3\n4\n")
				case "p":
					rom.write("109\n4\n4\n")
				case "u":
					rom.write("109\n5\n4\n")
			if "!" in statement1: #Transfer variable into register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("101\n4\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement1: #Transfer mem+rp to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("102\n4\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement1: #Transfer mem+ru to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("103\n4\n"),rom.write(statement3[1]),rom.write("\n")
			if statement1 == "stack":
				rom.write("118\n4\n")
		#----------------------REGISTER P ON SECOND * MOV ?,P * -------------------

		#----------------------REGISTER P ON FIRST * MOV P,? * -------------------
		if statement1 == "p": #Doing something to rx
			if "$" in statement2: #Transfer memory to it
				try:
					statement3 = statement2.split("$"[0])
				except:
					next
				rom.write("104\n4\n").rom.write(statement3[1]),rom.write("\n")
			match statement2: #Transfer register to register
				case "x":
					rom.write("109\n4\n1\n")
				case "y":
					rom.write("109\n4\n2\n")
				case "t":
					rom.write("109\n4\n3\n")
				case "p":
					rom.write("109\n4\n4\n")
				case "u":
					rom.write("109\n4\n5\n")
			if "!" in statement2: #Transfer variable into register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("104\n4\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement2: #Transfer mem+rp to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("105\n4\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement2: #Transfer mem+ru to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("106\n4\n"),rom.write(statement3[1]),rom.write("\n")
			if statement2 == "stack":
				rom.write("117\n4\n")
		#----------------------REGISTER P ON SECOND * MOV ?,P * -------------------
		#
		#
		#
		#
		#
		#
		#
		#----------------------REGISTER U ON SECOND * MOV ?,U * -------------------
		if statement2 == "u": #Doing something to rx
			if "#" in statement1: #Transfering value to it
				try:
					statement3 = statement1.split("#"[0])
				except:
					next
				rom.write("100\n5\n"),rom.write(statement3[1]),rom.write("\n")
			if "$" in statement1: #Transfer memory to it
				try:
					statement3 = statement1.split("$"[0])
				except:
					next
				rom.write("101\n5\n").rom.write(statement3[1]),rom.write("\n")
			match statement1: #Transfer register to register
				case "x":
					rom.write("109\n1\n5\n")
				case "y":
					rom.write("109\n2\n5\n")
				case "t":
					rom.write("109\n3\n5\n")
				case "p":
					rom.write("109\n4\n5\n")
				case "u":
					rom.write("109\n5\n5\n")
			if "!" in statement1: #Transfer variable into register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("101\n5\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement1: #Transfer mem+rp to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("102\n5\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement1: #Transfer mem+ru to register
				try:
					statement3 = statement1.split("!"[0])
				except:
					next
				rom.write("103\n5\n"),rom.write(statement3[1]),rom.write("\n")
			if statement1 == "stack":
				rom.write("118\n5\n")
		#----------------------REGISTER U ON SECOND * MOV ?,U * -------------------

		#----------------------REGISTER U ON FIRST * MOV U,? * -------------------
		if statement1 == "u": #Doing something to rx
			if "$" in statement2: #Transfer memory to it
				try:
					statement3 = statement2.split("$"[0])
				except:
					next
				rom.write("104\n5\n").rom.write(statement3[1]),rom.write("\n")
			match statement2: #Transfer register to register
				case "x":
					rom.write("109\n5\n1\n")
				case "y":
					rom.write("109\n5\n2\n")
				case "t":
					rom.write("109\n5\n3\n")
				case "p":
					rom.write("109\n5\n4\n")
				case "u":
					rom.write("109\n5\n5\n")
			if "!" in statement2: #Transfer variable into register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				address = getVariableAddress(statement3[1])
				rom.write("104\n5\n"),rom.write(str(address)),rom.write("\n")
			if "p%" in statement2: #Transfer mem+rp to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("105\n5\n"),rom.write(statement3[1]),rom.write("\n")
			if "u%" in statement2: #Transfer mem+ru to register
				try:
					statement3 = statement2.split("!"[0])
				except:
					next
				rom.write("106\n5\n"),rom.write(statement3[1]),rom.write("\n")
			if statement2 == "stack":
				rom.write("117\n5\n")
		#----------------------REGISTER U ON SECOND * MOV ?,U * -------------------

	if fullLine[0] == "jmp":
		statement1 = statements[0]

		if "!" in statement1:
			try:
				address_name = statement1.split("!"[0])
			except:
				next
			address_got = getLabelAddress(address_name[1])
			rom.write("110\n"),rom.write(str(address_got)),rom.write("\n")

		if "$" in statement1:
			try:
				address_pos	= statement1.split("$"[0])
			except:
				next
			rom.write("110\n"),rom.write(str(address_pos[1])),rom.write("\n")	

	if fullLine[0] == "inc":
		selected_register = fullLine[1]
		match selected_register:
			case "x":
				rom.write("107\n1\n")
			case "y":
				rom.write("107\n2\n")
			case "t":
				rom.write("107\n3\n")
			case "p":
				rom.write("107\n4\n")
			case "u":
				rom.write("107\n5\n")

	if fullLine[0] == "dec":
		selected_register = fullLine[1]
		match selected_register:
			case "x":
				rom.write("108\n1\n")
			case "y":
				rom.write("108\n2\n")
			case "t":
				rom.write("108\n3\n")
			case "p":
				rom.write("108\n4\n")
			case "u":
				rom.write("108\n5\n")

	if fullLine[0] == "beq":

		if "!" in fullLine[1]:
			try:
				address_name = statement1.split("!"[0])
			except:
				next
			address_got = getLabelAddress(address_name[1])
			rom.write("111\n"),rom.write(str(address_got)),rom.write("\n")

		if "$" in statement1:
			try:
				address_pos	= statement1.split("$"[0])
			except:
				next
			rom.write("111\n"),rom.write(str(address_pos[1])),rom.write("\n")

	if fullLine[0] == "bne":

		if "!" in fullLine[1]:
			try:
				address_name = statement1.split("!"[0])
			except:
				next
			address_got = getLabelAddress(address_name[1])
			rom.write("112\n"),rom.write(str(address_got)),rom.write("\n")

		if "$" in statement1:
			try:
				address_pos	= statement1.split("$"[0])
			except:
				next
			rom.write("112\n"),rom.write(str(address_pos[1])),rom.write("\n")

	if fullLine[0] == "den": # Display Enter
		rom.write("130\n")

	if fullLine[0] == "dbk": # Display Backspace
		rom.write("125\n")

	if fullLine[0] == "dcs": # Display clear
		rom.write("132\n")

	if fullLine[0] == "sef": # Set Equal Flag
		val = fullLine[1]
		rom.write("116\n"),rom.write(str(val)),rom.write("\n")

	if fullLine[0] == "nop": # No Operation
		rom.write("123\n")

	if fullLine[0] == "isp":
		rom.write("119\n")

	if fullLine[0] == "dsp":
		rom.write("120\n")

	if fullLine[0] == "ehi":
		rom.write("121\n")
	

	


		


			



	




		


		
			





		

	lc+=1
	if line == "return 0":
		break
