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

addressCounter = 0

#Array
arrayName = [0] * 10000
arrayLength = [0] * 10000

while 1:
    line = getline("cpl.txt",lc).rstrip("\n")
    fullLine = line.split()

    if fullLine[0] == "mk":
        name = fullLine[1]
        asm.write("*= !"),asm.write(str(name)),asm.write("\n")
    if fullLine[0] == "endFile":
        break

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
            length = int(fullLine[2])



    if fullLine[0] == "endFile":
        break

    lc+=1

asm.write(".var rx_cache *\n.var ry_cache *\n.var rt_cache *\n.var rp_cache *\n.var ru_cache *\n")
# Used by compiler
asm.write("//\n//\n*= !__cacheRX__\n    mov x,!rx_cache\n   mov y")



asm.write("return 0\n"),asm.close()
system('python3 speA.py')

