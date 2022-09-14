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

from os import system
from linecache import getline
from time import localtime

#Files
asm = open("asm.txt","w+")

#Time
n = localtime()

#Init Write
asm.write("//--------------------\n//Compiled Program\n//Compiled by: speC\n//Compiled Time: "),asm.write(str(n[3])),asm.write(":"),asm.write(str(n[4])),asm.write(":"),asm.write(str(n[5])),asm.write("\n//--------------------")
asm.write("\njmp $256 //Start\n*= $256 //Default Compiled Program Address\n")


lc=1

#Array
arrayName = [0] * 10000
arrayLength = [0] * 10000
arrayCount=0

def findArray(name):
    for x in range(10000):
        if name == arrayName[x]:
            break
    return arrayLength[x]

while 1:
    line = getline("cpl.txt",lc).rstrip("\n")
    fullLine = line.split()

    if fullLine[0] == "mk":
        name = fullLine[1]
        asm.write("*= !"),asm.write(str(name)),asm.write("\n")
    if fullLine[0] == "endFile":
        break

    if fullLine[0] == "do":
        pos = fullLine[1]
        asm.write(" jmp !"),asm.write(str(pos)),asm.write("\n")

    if fullLine[0] == "int":
        thing_name = fullLine[1]
        try:
            thing_number = fullLine[2].split(":"[0])
        except:
            next
        asm.write(" jsr !__cacheRX__\n  mov #"),asm.write(str(thing_number[1])),asm.write(",x\n    mov x,!"),asm.write(str(thing_name)),asm.write("\n   jsr !__retrieveRX__\n")

    if fullLine[0] == "print":
        print_string = ""
        print_string3 = ""
        for x in range(len(fullLine)):
            if x>0:
                print_string = print_string + " " + fullLine[x]
        try:
            print_string2 = print_string.split("("[0])
            print_string3 = print_string2[1].split(")"[0])
            print_string4 = print_string3[0].split(","[0])
        except:
            next
        for x in range(len(print_string4)):
            print(print_string4[x])
        for x in range(len(print_string4[x])):
            if "!" in print_string4[x]: # Int call
                try:
                    thing_var = print_string4[x].split("!"[0])
                except:
                    next
                print("VAR IS",thing_var)
                

            if "*" in print_string4[x]: # Array call
                next                    # Currently needs done, no function for now

        

    if "#" in fullLine[0]:
        next

    lc+=1

#Reset
lc=1

while 1:
    line = getline("cpl.txt",lc).rstrip("\n")
    fullLine = line.split()

    if fullLine[0] == "declare":
        thing_name = fullLine[1]
        if fullLine[2] == "int":
            asm.write(".var "),asm.write(str(thing_name)),asm.write(" *\n")
        if fullLine[2] == "array":
            thing_name = fullLine[1]
            length = int(fullLine[3])
            arrayName[arrayCount] = thing_name
            arrayLength[arrayCount] = length
            arrayCount+=1
            for x in range(length):
                asm.write(".var "),asm.write(str(thing_name) + str(x)),asm.write(" *\n")

    if fullLine[0] == "endFile":
        break

    if "#" in fullLine[0]:
        next

    lc+=1

asm.write(".var rx_cache *\n.var ry_cache *\n.var rt_cache *\n.var rp_cache *\n.var ru_cache *\n")


# Lets Write our register cache functions for the compiler to use
asm.write("//\n//\n*= !__cacheRegisters__\n    mov x,!rx_cache\n   mov y,!ry_cache\n   mov t,!rt_cache\n   mov p,!rp_cache\n   mov u,!ru_cache\n    rts\n")
asm.write("//\n//\n*= !__cacheRX__\n    mov x,!rx_cache\n   rts\n")
asm.write("//\n//\n*= !__cacheRY__\n    mov y,!ry_cache\n   rts\n")
asm.write("//\n//\n*= !__cahceRT__\n    mov t,!rt_cache\n   rts\n")
asm.write("//\n//\n*= !__cacheRP__\n    mov p,!rp_cache\n   rts\n")
asm.write("//\n//\n*= !__cacheRU__\n    mov u,!ru_cache\n   rts\n")
# Next
asm.write("//\n//\n*= !__retrieveRX__\n mov !rx_cache,x\n   rts\n")
asm.write("//\n//\n*= !__retrieveRY__\n mov !ry_cache,y\n   rts\n")
asm.write("//\n//\n*= !__retrieveRT__\n mov !rx_cache,t\n   rts\n")
asm.write("//\n//\n*= !__retrieveRP__\n mov !rp_cache,p\n   rts\n")
asm.write("//\n//\n*= !__retrieveRU__\n mov !ru_cache,u\n   rts\n")






asm.write("return 0\n"),asm.close()
system('python3 speA.py')

