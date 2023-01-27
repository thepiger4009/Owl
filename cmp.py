#compiler.py
"""
Owl Compiler
Build: 1.0
Date: 12-12-22
Author: Landon Smith

____________________________

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
from pyparsing import Char

#Files
asm = open("asm.txt","w+")

#Time
n = localtime()

#Init Write
asm.write("*= $1024\n")

# Filter function
def filterString(inputString,word):
    filterString = inputString.split()
    for x in range(len(filterString)):
        if filterString[x] == word:
            next
        else:
            finalString = finalString + filterString[x]
        return finalString


lc=1
ifc = 0  # IF COUNTER
mifc = 0 #Multiple if Counter
forc = 0 # FOR COUNTER
firstIFc = 0 # First If Counter, USED IF DETECTED MULTIPLE
ifCounter = 0
inputCounter = 0

while True:
    line = getline("program.opl",lc).rstrip("\n")
    fullLine = line.split()
    try:
        if fullLine[0] == "lol":
            next
    except:
        fullLine = ["//"] * 2
    if fullLine[0] == "make":
        name = fullLine[1].split("("[0])
        name = name[0].split(")"[0])
        asm.write("*= !"+name[0]+"\n")
    """
    if "!" in fullLine[0]:
        name=fullLine[0].split("!"[0])
        name=name[1]
        asm.write(".var "+name+" *\n")
        if fullLine[1] == "=":
            if "!" in fullLine[1]:
                nov = fullLine[2].split("!"[0])+
                nov = nov[1]
            else:
                nov = fullLine[2]
            if fullLine[3] == "+":
                if "!" in fullLine[4]:
                    next
                elif "$" in fullLine[4]:
                    next    
                else:
                    next
            elif fullLine[3] == "-":
                next
            else:
                asm.write("mov #"+nov+",x\nmov x,!"+name+"\nmov #0,x\n") 
    """
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

    if "_" in fullLine[0]:
        firstWord = fullLine[0].split("_"[0])
        fullLine[0] = firstWord[1]
        for x in range(len(fullLine)):
            asm.write(fullLine[x]),asm.write(" ")
        asm.write("\n")
    if fullLine[0] == "if":

        if fullLine[1] == "input":
            if fullLine[2] == "=":
                input_string = ""
                for x in range(len(fullLine)):
                    if fullLine[x] == "if":
                        next
                    elif fullLine[x] == "input":
                        next
                    elif fullLine[x] == "=":
                        next
                    elif fullLine[x] == "{":
                        next
                    else:
                        input_string = input_string + fullLine[x] + " "
                print("[compiler]: IFINPUT String:",input_string)
                asm.write("jmp !inputIfKeyCheck"+str(inputCounter)+"\n.var inputIfKeyC"+str(inputCounter)+" *\n*= !inputIfKeyCheck"+str(inputCounter)+"\nmov $524287,x\ncmp x,#0\nbeq !inputIfKeyCheck"+str(inputCounter)+"\nbne !inputIfStateCheck"+"\n*= !inputIfStateCheck\n")
                for x in range(len(input_string)):
                    asm.write("cmp p,#"+str(x)+"\nbeq !inputIfState"+str(x)+"\n")
                for x in range(len(input_string)):
                    asm.write("*= !inputIfState"+str(x)+"\ninc p\nmov #0,x\nmov x,$524287\njmp !inputIfStateCheck\ncmp x,#"+str(ord(input_string[x]))+"\nbeq !inputIfState\nbne !inputIfKeyCheck"+str(inputCounter)+"\n")
                inputCounter+=1
        
            
        if "&" in fullLine[1]:
            arrayName = fullLine[1].split("&"[0])
            type = (''.join(x for x in fullLine[1] if x.isdigit()))
            asm.write("mov !"+arrayName[1]+",y\n")

            if fullLine[2] == "=":
                von = fullLine[3] # VARIABLE OR NUMBER
                if "!" in von:
                    next
                elif "@" in von:
                    character = von.split("@"[0])
                    asm.write("cmp y,#"+str(ord(character[1]))+"\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                    asm.write("*= !doIf"+str(ifc)+"\n")
                else:
                    asm.write("cmp y,#"+von+"\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                    asm.write("*= !doIf"+str(ifc)+"\n")


        if "!" in fullLine[1]:
            varName = fullLine[1].split("!"[0])
            asm.write("mov !"+varName[1]+",y\n")
            if fullLine[2] == "=":
                von = fullLine[3] # VARIABLE OR NUMBER
                if "!" in von:
                    next
                elif "@" in von:
                    character = von.split("@"[0])
                    sc = Char(character[1])
                    asm.write("cmp y,#"+str(ord(character[1]))+"\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                    asm.write("*= !doIf"+str(ifc)+"\n")
                else:
                    asm.write("cmp y,#"+von+"\nbne !AfterIf"+str(ifc)+"\nbeq !doIf"+str(ifc)+"\n")
                    asm.write("*= !doIf"+str(ifc)+"\n")

    if fullLine[0] == "};;":
        asm.write("*= !AfterIf"+str(ifc+ifCounter)+"\n")
        ifc+=1
# if @array[1] to 50 = @lodon



    if fullLine[0] == "int":
        name = fullLine[1]
        type = fullLine[2]
        if type == ":=":
            von = fullLine[3]
            if von == "+":
                var = von.split("!"[0])
                if "!" in fullLine[4]:
                    next
                elif "$" in fullLine[4]:
                    next
                else:
                    val = fullLine[4]
                    asm.write("mov !"+name+",x\nmov #"+str(val)+",y\nadd x,y\n mov y,!"+name+"\n")
            if von == "-":
                var = von.split("!"[0])
                if "!" in fullLine[4]:
                    next
                elif "$" in fullLine[4]:
                    next
                else:
                    val = fullLine[4]
                    asm.write("mov !"+name+",x\nmov #"+str(val)+",y\nsub x,y\n mov y,!"+name+"\n")
                
            if "!" in von:
                var = von.split("!"[0])
                asm.write("mov !"+str(var[1])+",x\n")
                try:
                    if fullLine[4] == "t":
                        next
                except:
                    fullLine = ["//"] * 10
                if fullLine[4] == "+":
                    val = fullLine[5]
                    asm.write("mov #"+str(val)+",y\nadd x,y\nmov x,!"+name+"\n")
                else:
                    asm.write("mov x,!"+name+"\n")
            elif "$" in von:
                address = von.split("$"[0])
                asm.write("mov $"+str(address[1])+",x\nmov x,!"+name+"\n")
            elif "#" in von:
                num=von.split("#"[0])
                asm.write("mov #"+str(num[1])+",x\n")
                try:
                    if fullLine[4] == "t":
                        next
                except:
                    fullLine = ["//"] * 10
                if fullLine[4] == "+":
                    val = fullLine[5]
                    asm.write("mov #"+str(val)+",y\nadd x,y\nmov x,!"+name+"\n")
                else:
                    asm.write("mov x,!"+name+"\n")



    if "array" in fullLine[0]:
        num = (''.join(x for x in fullLine[0] if x.isdigit()))
        print("[Compiler]: Array has length of",num)
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
        if "!" in fullLine[1]:
            FORvar = fullLine[1].split("!"[0])
            if fullLine[2] == "to":
                if "!" in fullLine[3]:
                    next   # VAR NEEDS WORKED ON
                else:
                    FORnum = fullLine[3]
                    asm.write("mov #0,p\n*= !forLoop"+str(forc)+"\nmov !"+FORvar[1]+",t\ninc p\n")

        else:
            asm.write("*= !forLoop"+str(forc)+"\n")

    if fullLine[0] == "};;;": #END for
        n = int(FORnum) - 1
        asm.write("cmp t,#"+str(n)+"\nbeq !afterFor"+str(forc)+"\nmov p,!"+FORvar[1]+"\nbne !forLoop"+str(forc)+"\n")
        asm.write("*= !afterFor"+str(forc)+"\n")
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

    if fullLine[0] == "go":
        if "$" in fullLine[1]:
            address=fullLine[1].split("$"[0])
            asm.write("jmp $"+address[1]+"\n")
        else:
            functionGiven = fullLine[1]
            asm.write("jmp !"+functionGiven+"\n")

    if fullLine[0] == "};":
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
    line = getline("program.opl",lc).rstrip("\n")
    fullLine = line.split()
    try:
        if fullLine[0] == "lol":
            next
    except:
        fullLine = ["//"] * 2
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

asm.write("return 0"),asm.close(),system('python3 asm.py')

