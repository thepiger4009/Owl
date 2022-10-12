#~/speC.py
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

from array import ArrayType
from os import system
from linecache import getline
from time import localtime

#Files
asm = open("asm.txt","w+")

#Time
n = localtime()

#Init Write
asm.write("//--------------------\n//Compiled Program\n//Compiled by: speC\n//Compiled Time: "),asm.write(str(n[3])),asm.write(":"),asm.write(str(n[4])),asm.write(":"),asm.write(str(n[5])),asm.write("\n//--------------------")
asm.write("\n//Start\n*= $256 //Default Compiled Program Address\n")


lc=1
ifc = 0  # IF COUNTER
forc = 0 # FOR COUNTER
firstIFc = 0 # First If Counter, USED IF DETECTED MULTIPLE

while True:
    line = getline("cpl.txt",lc).rstrip("\n")
    fullLine = line.split()
    if fullLine[0] == "make":
        name = fullLine[1].split("("[0])
        name = name[0].split(")"[0])
        asm.write("*= !"+name[0]+"\n")
    if fullLine[0] == "declare":
        name = fullLine[1]
        type = fullLine[2]
        ask = fullLine[3]
        if type == "int":
            if ask == ":=":
                askresult = fullLine[4]
                asm.write("mov #"+askresult+",x\nmov x,!"+name+"\n")
        if "array" in type:
            amount = (''.join(x for x in type if x.isdigit()))
            if ask == ":=":
                askresult = fullLine[4]
                asm.write("mov #"+askresult + ",x\n")
                for x in range(int(amount)):
                    asm.write("mov x,!"+name+str(x)+"\n")

    if fullLine[0] == "if":
        if "&" in fullLine[1]:
            arrayName = fullLine[1].split("&"[0])
            type = (''.join(x for x in fullLine[1] if x.isdigit()))
            asm.write("mov !"+varName[1]+type+"\n")

        if "!" in fullLine[1]:
            varName = fullLine[1].split("!"[0])
            asm.write("mov !"+varName[1]+",y\n")
            if fullLine[2] == "=":
                von = fullLine[3] # VARIABLE OR NUMBER
                if "!" in von:
                    next
                elif "@" in von:
                    character = von.split("@"[0])
                    match character[1]:
                        case "q":
                            asm.write("cmp y,#113\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "w":
                            asm.write("cmp y,#119\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "e":
                            asm.write("cmp y,#101\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "r":
                            asm.write("cmp y,#114\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "t":
                            asm.write("cmp y,#116\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "y":
                            asm.write("cmp y,#121\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "u":
                            asm.write("cmp y,#117\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "i":
                            asm.write("cmp y,#105\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "o":
                            asm.write("cmp y,#111\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "p":
                            asm.write("cmp y,#112\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "a":
                            asm.write("cmp y,#97\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "s":
                            asm.write("cmp y,#115\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "d":
                            asm.write("cmp y,#100\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "f":
                            asm.write("cmp y,#102\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "g":
                            asm.write("cmp y,#103\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "h":
                            asm.write("cmp y,#104\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "j":
                            asm.write("cmp y,#106\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "k":
                            asm.write("cmp y,#107\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "l":
                            asm.write("cmp y,#108\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "z":
                            asm.write("cmp y,#122\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "x":
                            asm.write("cmp y,#120\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "c":
                            asm.write("cmp y,#99\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "v":
                            asm.write("cmp y,#118\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "b":
                            asm.write("cmp y,#98\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "n":
                            asm.write("cmp y,#110\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                        case "m":
                            asm.write("cmp y,#109\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                            asm.write("*= !doIf"+str(ifc)+"\n")
                else:
                    asm.write("cmp y,#"+von+"\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                    asm.write("*= !doIf"+str(ifc)+"\n")

    if fullLine[0] == "endIf":
        asm.write("*= !AfterIf"+str(ifc)+"\n")
        ifc+=1

    if fullLine[0] == "int":
        name = fullLine[1]
        type = fullLine[2]
        if type == ":=":
            von = fullLine[3]
            if "!" in von:
                var = von.split("!"[0])
                asm.write("mov !"+str(var[1])+",x\nmov x,!"+name+"\n")
            elif "$" in von:
                address = von.split("$"[0])
                asm.write("mov $"+str(address[1])+",x\nmov x,!"+name+"\n")
            else:
                asm.write("mov #"+str(von)+",x\nmov x,!"+name+"\n")

    if "array" in fullLine[0]:
        num = (''.join(x for x in fullLine[0] if x.isdigit()))
        name = fullLine[1]
        type = fullLine[2]
        if type == ":=":
            if "!" in fullLine[3]:
                var = fullLine[3].split("!"[0])
                asm.write("mov !"+str(var[1])+",x\nmov x,!"+name+str(num)+"\n")
            elif "$" in fullLine[3]:
                address = fullLine[3].split("$"[0])
                asm.write("mov $"+str(address[1])+",x\nmov x,!"+name+str(num)+"\n")
            else:
                asm.write("mov #"+fullLine[3]+",x\nmov x,!"+name+str(num)+"\n")

    if fullLine[0] == "printsp":
        asm.write("dsn\n")

    if fullLine[0] == "backspace":
        asm.write("dbk\n")



    if fullLine[0] == "for":
        if "!" in fullLine[1]: # VAR NEEDS WORK
            next 
        else:
            asm.write("*= !forLoop"+str(forc)+"\n")

    if fullLine[0] == "endFor":
        asm.write("jmp !forLoop"+str(forc)+"\n")
        forc+=1

    if fullLine[0] == "/*":
        asm.write("//"+fullLine[1]+"\n")

    if fullLine[0] == "address":
        addressLocated = fullLine[1]
        type = fullLine[2]
        if type == ":=":
            von = fullLine[3]
            if "!" in von: # NEEDS DONE: ADDRESS 5454 := !toys
                next
            else:
                asm.write("mov #"+str(von)+",x\nmov x,$"+addressLocated+"\n")

    if fullLine[0] == "do":
        functionGiven = fullLine[1]
        asm.write("jsr !"+functionGiven+"\n")

    if fullLine[0] == "end":
        asm.write("rts\n")

    if fullLine[0] == "println":
        print_string = ""
        for x in range(len(fullLine)):
            if fullLine[x] == "println":
                next
            else:
                print_string = print_string + fullLine[x] + " "
        print_string = print_string.split()
        print(print_string)
        y=0
        for x in range(len(print_string)):
            for y in range(len(print_string[x])):
                asm.write("mov #"+str(ord(print_string[x][y]))+",x\ndra x\n")
            asm.write("mov #32,x\ndra x\n")
        asm.write("den\n")

    if fullLine[0] == "print":
        print_string = ""
        for x in range(len(fullLine)):
            if fullLine[x] == "print":
                next
            else:
                print_string = print_string + fullLine[x] + " "
        print_string = print_string.split()
        y=0
        for x in range(len(print_string)):
            for y in range(len(print_string[x])):
                asm.write("mov #"+str(ord(print_string[x][y]))+",x\ndra x\n")
            asm.write("mov #32,x\ndra x\n")

    if fullLine[0] == "printns":
        print_string = ""
        for x in range(len(fullLine)):
            if fullLine[x] == "printns":
                next
            else:
                print_string = print_string + fullLine[x] + " "
        print_string = print_string.split()
        print(print_string)
        y=0
        for x in range(len(print_string)):
            for y in range(len(print_string[x])):
                asm.write("mov #"+str(ord(print_string[x][y]))+",x\ndra x\n")

    

    
            

    

            

    

          

    if line == "return 0":
        break
    if "//" in fullLine[0]:
        next
    lc+=1

lc = 1
while True:
    line = getline("cpl.txt",lc).rstrip("\n")
    fullLine = line.split()
    if fullLine[0] == "declare":
        name = fullLine[1]
        type = fullLine[2]
        ask = fullLine[3]
        if type == "int":
            if ask == ":=":
                askresult = fullLine[4]
            asm.write(".var "+name+" *\n")
        if "array" in type:
            amount = (''.join(x for x in type if x.isdigit()))
            if ask == ":=":
                askresult = fullLine[4]
            for x in range(int(amount)):
                asm.write(".var "+ name + str(x)+" *\n")
          

    if line == "return 0":
        break
    if "//" in fullLine[0]:
        next
    lc+=1

asm.write("return 0"),asm.close(),system('python3 speA.py')

