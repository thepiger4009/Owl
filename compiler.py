#compiler.py
"""
Owl Virtual Machine Compiler
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
from tabnanny import check
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
multiplyCounter = 0
forCounter = 0
ifCounter = 0
ifbefore = 0
inputCounter = 0
global variableList
variableList = [0] * 1000
global vcc
vcc = 0

def check_var(name):
    for x in range(1000):
        if variableList[x] == name:
            return True

def declare_var(name):
    global vcc
    variableList[vcc] = name
    vcc+=1

while 1:
    line = getline("program.opl",lc).rstrip("\n")
    fullLine = line.split()
    try:
        if fullLine[0] == "lol":
            next
    except:
        fullLine = ["//"] * 2

    if "_" in fullLine[0]:
        firstWord = fullLine[0].split("_"[0])
        fullLine[0] = firstWord[1]
        for x in range(len(fullLine)):
            asm.write(fullLine[x]),asm.write(" ")
        asm.write("\n")

    if "$" in fullLine[0] and fullLine[1] == "#":
        number = fullLine[1].strip("#"[0])
        address = fullLine[0].strip("$"[0])
        asm.write("mov #"+number+",x\nmov x,$"+address+"\n")

    if fullLine[0] == "for" and fullLine[2] == "=" and "#" in fullLine[3] and fullLine[4] == "to" and "#" in fullLine[5]:
        forvar = fullLine[1]
        forvar=forvar
        fornum = fullLine[3].strip("#"[0])
        forNum = fullLine[5].strip("#"[0])
        if check_var(var) == True:
            next
        else:
            declare_var(forvar)
            print("[compiler]: Variable",forvar,"is created.")
        asm.write("mov #1,y, mov !"+forvar+",t\nmov #"+fornum+",p\nmov p,!"+forvar+"\n*= !forLoop"+str(forCounter)+"\nmov !"+forvar+",t\ninc p\nadd y,t\n")
    if fullLine[0] == "};;;":
        asm.write("cmp p,#"+str(forNum)+"\nbeq !afterFor"+str(forCounter)+"\nmov p,!"+forvar[1]+"\nbne !forLoop"+str(forCounter)+"\n")
        asm.write("*= !afterFor"+str(forCounter)+"\nmov t,!"+forvar+"\n")
        forCounter+=1




    if fullLine[0] == "if":
        ifCounter+=1
        var = fullLine[1]
        asm.write("mov !"+var+",y\n")

        if fullLine[2] == "=":
            if "#" in fullLine[3]:
                ifnum = fullLine[3].split("#"[0])
                ifnum=ifnum[1]

                asm.write("cmp y,#"+str(ifnum)+"\nbne !AfterIf"+str(ifCounter)+"\nbeq !doIf"+str(ifCounter)+"\n")
                asm.write("*= !doIf"+str(ifCounter)+"\n")

            if "@" in fullLine[3]:
                ifnum = fullLine[3].split("@"[0])
                ifnum=ifnum[1]

                asm.write("cmp y,#"+str(ord(ifnum))+"\nbne !AfterIf"+str(ifCounter)+"\nbeq !doIf"+str(ifCounter)+"\n")
                asm.write("*= !doIf"+str(ifCounter)+"\n")

    if fullLine[0] == "};;}":
        asm.write("*= !AfterIf"+str(ifCounter)+"\n")
        ifCounter-=1
    if fullLine[0] == "};;":
        asm.write("*= !AfterIf"+str(ifCounter)+"\n")
        


    

    if fullLine[0] == "};":
        asm.write("jmp !cmpendloop\n")
    if fullLine[0] == "};}":
        asm.write("rts\n")
        


    if fullLine[0] == "clear":
        asm.write("dcs\n")

    if fullLine[0] == "do":
        section_name = fullLine[1].split(";"[0])
        section_name=section_name[0]
        asm.write("jsr !"+section_name+"\n")

    try:
        if fullLine[0] == "print":
            bg = 0
            for x in range(len(fullLine)):
                if fullLine[x] == "+":
                    asm.write("mov #32,x\ndra x\n")
                if "!" in fullLine[x]:
                    var = fullLine[x].split("!"[0])
                    var=var[1]
                    asm.write("mov !"+var+",x\ndrv x\n")
                else:
                    if bg == 1:
                        for y in range(len(fullLine[x])):
                            asm.write("mov #"+str(ord(fullLine[x][y]))+",x\ndra x\n")
                        asm.write("mov #32,x\ndra x\n")
                bg=1
                    


    except:
        next

    try:

        if fullLine[1] == "+=":
            var=fullLine[0]

            if "#" in fullLine[2]:
                var_num1 = fullLine[2].strip("#"[0])
                var_num1=var_num1
                print("___________________________________________")
                if check_var(var) == True:
                    asm.write("mov !"+var+",x\nmov #"+var_num1+",y\nadd x,y\nmov y,!"+var+"\n")
                    print("[compiler]: Variable",var,"is adding",var_num1,"to itself.")
                else:
                    declare_var(var)
                    asm.write("mov !"+var+",x\nmov #"+var_num1+",y\nadd x,y\nmov y,!"+var+"\n")
                    print('[compiler]: Variable',var,"is created.")
                    print("[compiler]: Variable",var,"is  adding",var_num1,"to itself.")
                print("___________________________________________")

            if "!" in fullLine[2]:
                var2 = fullLine[2].strip("!"[0])
                var2=var2
                print("___________________________________________")
                if check_var(var) == True:
                    asm.write("mov !"+var+",x\nmov !"+var2+",y\nadd x,y\nmov y,!"+var+"\n")
                    print("[compiler]: Variable",var,"is adding variable",var2,"to itself.")
                    if check_var(var2) == True:
                        next
                    else:
                        declare_var(var2)
                        print('[compiler warn]: Created',var2,"since it didn't exist.")
                else:
                    declare_var(var)
                    asm.write("mov !"+var+",x\nmov #"+var+",y\nadd x,y\nmov y,!"+var+"\n")
                    print('[compiler]: Variable',var,"is created.")
                    print("[compiler]: Variable",var,"is adding variable",var2,"to itself.")
                    if check_var(var2) == True:
                        next
                    else:
                        declare_var(var2)
                        print('[compiler warn]: Created',var2,"since it didn't exist.")
                print("___________________________________________")

        if fullLine[1] == "-=":
            var=fullLine[0]

            if "#" in fullLine[2]:
                var_num1 = fullLine[2].strip("#"[0])
                var_num1=var_num1
                print("___________________________________________")
                if check_var(var) == True:
                    asm.write("mov !"+var+",x\nmov #"+var_num1+",y\nsub y,x\nmov x,!"+var+"\n")
                    print("[compiler]: Variable",var,"is subtracting",var_num1,"from itself.")
                else:
                    declare_var(var)
                    asm.write("mov !"+var+",x\nmov #"+var_num1+",y\nsub y,x\nmov x,!"+var+"\n")
                    print('[compiler]: Variable',var,"is created.")
                    print("[compiler]: Variable",var,"is  subtracting",var_num1,"from itself.")
                print("___________________________________________")

            if "!" in fullLine[2]:
                var2 = fullLine[2].strip("!"[0])
                var2=var2
                print("___________________________________________")
                if check_var(var) == True:
                    asm.write("mov !"+var+",x\nmov !"+var2+",y\nsub y,x\nmov x,!"+var+"\n")
                    print("[compiler]: Variable",var,"is subtracting variable",var2,"from itself.")
                    if check_var(var2) == True:
                        next
                    else:
                        declare_var(var2)
                        print('[compiler warn]: Created',var2,"since it didn't exist.")
                else:
                    declare_var(var)
                    asm.write("mov !"+var+",x\nmov #"+var+",y\nsub y,x\nmov x,!"+var+"\n")
                    print('[compiler]: Variable',var,"is created.")
                    print("[compiler]: Variable",var,"is subtracting variable",var2," itself.")
                    if check_var(var2) == True:
                        next
                    else:
                        declare_var(var2)
                        print('[compiler warn]: Created',var2,"since it didn't exist.")
                print("___________________________________________")
                
    except:
        next

    try:
        if fullLine[1] == "=": #Expecting a variable declaration or change
            var=fullLine[0]

            if "$" in fullLine[2] and fullLine[3] == ";":
                print("___________________________________________")
                address=fullLine[2].strip("$"[0])
                address=address
                asm.write("mov $"+str(address)+",x\nmov x,!"+var+"\n")
                if check_var(var) == True:
                    next
                else:
                    declare_var(var)
                    print("[compiler]: Variable",var,"is created.")
                print("[compiler]: Variable",var,"now equals address $"+address+".")
                print("___________________________________________")

            if "!" in fullLine[2] and fullLine[3] == ";":
                print("___________________________________________")
                var2=fullLine[2].strip("!"[0])
                asm.write("mov !"+var2+",x\nmov x,!"+var+"\n")
                print('[compiler]: Variable',var,"now equals variable",var2)
                if check_var(var) == True:
                    next
                else:
                    declare_var(var)
                    print("[compiler]: Variable",var,"is created.")
                if check_var(var2) == True:
                    next
                else:
                    declare_var(var2)
                    print('[compiler warn]: Created',var2,"since it didn't exist.")
                print("___________________________________________")

            if "!" in fullLine[2] and fullLine[3] == "+" and "!" in fullLine[4]:
                var1 = fullLine[2].strip("!"[0])
                var2 = fullLine[4].strip("!"[0])
                print("___________________________________________")
                asm.write("mov !"+var1+",x\nmov !"+var2+",y\nadd x,y\nmov y,!"+var+"\n")
                if check_var(var) == True:
                    next
                else:
                    declare_var(var)
                    print("[compiler]: Variable",var,"is created.")
                if check_var(var1) == True:
                    next
                else:
                    declare_var(var1)
                    print("[compiler warn]: Created",var1,"since it didn't exist.")
                if check_var(var2) == True:
                    next
                else:
                    declare_var(var2)
                    print('[compiler warn]: Created',var2,"since it dind't exist.")
                print("[compiler]: Variable",var,"is now equal to variable",var1,"+",var2)
                print("___________________________________________")

            if "!" in fullLine[2] and fullLine[3] == "-" and "!" in fullLine[4]:
                var1 = fullLine[2].strip("!"[0])
                var2 = fullLine[4].strip("!"[0])
                print("___________________________________________")
                asm.write("mov !"+var1+",x\nmov !"+var2+",y\nsub y,x\nmov x,!"+var+"\n")
                if check_var(var) == True:
                    next
                else:
                    declare_var(var)
                    print("[compiler]: Variable",var,"is created.")
                if check_var(var1) == True:
                    next
                else:
                    declare_var(var1)
                    print("[compiler warn]: Created",var1,"since it didn't exist.")
                if check_var(var2) == True:
                    next
                else:
                    declare_var(var2)
                    print('[compiler warn]: Created',var2,"since it dind't exist.")
                print("[compiler]: Variable",var,"is now equal to variable",var1,"",var2)
                print("___________________________________________")

            if "!" in fullLine[2] and fullLine[3] == "-" and "#" in fullLine[4]:
                var1 = fullLine[2].strip("!"[0])
                var_num1 = fullLine[4].strip("#"[0])
                print("___________________________________________")
                asm.write("mov !"+var1+",x\nmov #"+var_num1+",y\nsub y,x\nmov x,!"+var+"\n")
                if check_var(var) == True:
                    next
                else:
                    declare_var(var)
                    print("[compiler]: Variable",var,"is created.")
                if check_var(var1) == True:
                    next
                else:
                    declare_var(var1)
                    print("[compiler warn]: Created",var1,"since it didn't exist.")
                if check_var(var2) == True:
                    next
                else:
                    declare_var(var2)
                    print('[compiler warn]: Created',var2,"since it dind't exist.")
                print("[compiler]: Variable",var,"is now equal to variable",var1,"",var2)

            if "!" in fullLine[2] and fullLine[3] == "+" and "#" in fullLine[4]:
                var1 = fullLine[2].strip("!"[0])
                var_num1 = fullLine[4].strip("#"[0])
                print("___________________________________________")
                asm.write("mov !"+var1+",x\nmov #"+var_num1+",y\nadd x,y\nmov x,!"+var+"\n")
                if check_var(var) == True:
                    next
                else:
                    declare_var(var)
                    print("[compiler]: Variable",var,"is created.")
                if check_var(var1) == True:
                    next
                else:
                    declare_var(var1)
                    print("[compiler warn]: Created",var1,"since it didn't exist.")
                if check_var(var2) == True:
                    next
                else:
                    declare_var(var2)
                    print('[compiler warn]: Created',var2,"since it dind't exist.")
                print("[compiler]: Variable",var,"is now equal to variable",var1,"",var2)

            if "#" in fullLine[2] and fullLine[3] == "+" and "!" in fullLine[4]:
                var1 = fullLine[4].strip("!"[0])
                var_num1 = fullLine[2].strip("#"[0])
                print("___________________________________________")
                asm.write("mov !"+var1+",x\nmov #"+var_num1+",y\nadd y,x\nmov x,!"+var+"\n")
                if check_var(var) == True:
                    next
                else:
                    declare_var(var)
                    print("[compiler]: Variable",var,"is created.")
                if check_var(var1) == True:
                    next
                else:
                    declare_var(var1)
                    print("[compiler warn]: Created",var1,"since it didn't exist.")
                if check_var(var2) == True:
                    next
                else:
                    declare_var(var2)
                    print('[compiler warn]: Created',var2,"since it dind't exist.")
                print("[compiler]: Variable",var,"is now equal to variable",var1,"",var2)

            if "#" in fullLine[2] and fullLine[3] == "-" and "!" in fullLine[4]:
                var1 = fullLine[4].strip("!"[0])
                var_num1 = fullLine[2].strip("#"[0])
                print("___________________________________________")
                asm.write("mov !"+var1+",x\nmov #"+var_num1+",y\nsub x,y\nmov y,!"+var+"\n")
                if check_var(var) == True:
                    next
                else:
                    declare_var(var)
                    print("[compiler]: Variable",var,"is created.")
                if check_var(var1) == True:
                    next
                else:
                    declare_var(var1)
                    print("[compiler warn]: Created",var1,"since it didn't exist.")
                if check_var(var2) == True:
                    next
                else:
                    declare_var(var2)
                    print('[compiler warn]: Created',var2,"since it dind't exist.")
                print("[compiler]: Variable",var,"is now equal to variable",var1,"",var2)




            if "#" in fullLine[2] and fullLine[3] == ";":
                var_num1 = fullLine[2].split("#"[0])
                var_num1=var_num1[1]
                print("___________________________________________")
                asm.write("mov #"+var_num1+",x\nmov x,!"+var+"\n")
                if check_var(var) == True:
                    print('[compiler]: Variable',var,"is being modified!")
                else:
                    print('[compiler]: Variable',var,"is created."),print('[compiler]: Variable',var,"is being modified!")
                    declare_var(var)
                print('[compiler]:',var,"now equals",var_num1)
                print("___________________________________________")
    except:
        next
            

    if fullLine[0] == "call":
        call_name = fullLine[1].split(';'[0])
        call_name=call_name[0]
        asm.write('jsr !'+call_name+"\n")
    if fullLine[0] == 'go':
        go_name = fullLine[1].split(';'[0])
        go_name=go_name[0]
        asm.write('jmp !'+go_name+"\n")

    if fullLine[0] == "section":
        section_name = fullLine[1].split(';'[0])
        section_name=section_name[0]
        section_vars = fullLine[2].split(','[0])
        asm.write("*= !"+section_name+"\n")
        print("___________________________________________"),print("[compiler]: Section declared:",section_name),print("[compiler]: Variables declared(",section_vars,")"),print("___________________________________________")
        if section_vars[0] == 'void':
            print('[compiler]: Section',section_name,'variables voided.')
        else:
            for x in range(len(section_vars)):
                if check_var(section_vars[x]) == True:
                    print('[compiler]: Variable',section_vars[x],"already exists, ignoring.")
                else:
                    declare_var(section_vars[x])
                    print('[compiler]: Variable',section_vars[x],'added.')
        print('[compiler]: VCC should now be',vcc),print("___________________________________________")
    lc+=1
    if fullLine[0] == "*endfile":
        break

for x in range(1000):
    if variableList[x] == 0:
        next
    else:
        asm.write(".var "+variableList[x]+' *\n')
asm.write("*= !cmpendloop\njmp !cmpendloop\n")
asm.write(".var compilerTemp *\nreturn 0")
asm.close()
system('python3 asm.py')