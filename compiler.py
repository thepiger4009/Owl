#~/compiler.py
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
from pyparsing import Char

#Files
asm = open("asm.txt","w+")

#Time
n = localtime()

#Init Write
asm.write("//--------------------\n//Compiled Program\n//Compiled Time: "),asm.write(str(n[3])),asm.write(":"),asm.write(str(n[4])),asm.write(":"),asm.write(str(n[5])),asm.write("\n//--------------------")
asm.write("\n//Start\n*= $256 //Default Compiled Program Address\n")

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
inputIfCounter = 0

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
                new_string = ""
                givenString = fullLine[3]
                asm.write("*= !setupInput\nmov #0,x\nmov x,!key\nmov #0,x\nmov x,!keyPress\nmov #0,x\nmov x,!keyCount\nmov #0,x\nmov x,!word0\nmov x,!word1\nmov x,!word2\nmov x,!word3\nmov x,!word4\nmov x,!word5\nmov x,!word6\nmov x,!word7\nmov x,!word8\nmov x,!word9\nmov x,!word10\nmov x,!word11\nmov x,!word12\nmov x,!word13\nmov x,!word14\nmov x,!word15\nmov x,!word16\nmov x,!word17\nmov x,!word18\nmov x,!word19\nmov x,!word20\nmov x,!word21\nmov x,!word22\nmov x,!word23\nmov x,!word24\nmov x,!word25\nmov x,!word26\nmov x,!word27\nmov x,!word28\nmov x,!word29\nmov x,!word30\nmov x,!word31\nmov x,!word32\nmov x,!word33\nmov x,!word34\nmov x,!word35\nmov x,!word36\nmov x,!word37\nmov x,!word38\nmov x,!word39\njsr !inputLoop\nrts\n*= !inputLoop\nmov $524287,x\nmov x,!key\nmov !key,y\ncmp y,#113\nbne !AfterIf0\nbeq !doIf0\n*= !doIf0\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf0\nmov !key,y\ncmp y,#119\nbne !AfterIf1\nbeq !doIf1\n*= !doIf1\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf1\nmov !key,y\ncmp y,#101\nbne !AfterIf2\nbeq !doIf2\n*= !doIf2\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf2\nmov !key,y\ncmp y,#114\nbne !AfterIf3\nbeq !doIf3\n*= !doIf3\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf3\nmov !key,y\ncmp y,#116\nbne !AfterIf4\nbeq !doIf4\n*= !doIf4\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf4\nmov !key,y\ncmp y,#121\nbne !AfterIf5\nbeq !doIf5\n*= !doIf5\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf5\nmov !key,y\ncmp y,#117\nbne !AfterIf6\nbeq !doIf6\n*= !doIf6\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf6\nmov !key,y\ncmp y,#105\nbne !AfterIf7\nbeq !doIf7\n*= !doIf7\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf7\nmov !key,y\ncmp y,#111\nbne !AfterIf8\nbeq !doIf8\n*= !doIf8\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf8\nmov !key,y\ncmp y,#112\nbne !AfterIf9\nbeq !doIf9\n*= !doIf9\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf9\nmov !key,y\ncmp y,#97\nbne !AfterIf10\nbeq !doIf10\n*= !doIf10\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf10\nmov !key,y\ncmp y,#115\nbne !AfterIf11\nbeq !doIf11\n*= !doIf11\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf11\nmov !key,y\ncmp y,#100\nbne !AfterIf12\nbeq !doIf12\n*= !doIf12\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf12\nmov !key,y\ncmp y,#102\nbne !AfterIf13\nbeq !doIf13\n*= !doIf13\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf13\nmov !key,y\ncmp y,#103\nbne !AfterIf14\nbeq !doIf14\n*= !doIf14\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf14\nmov !key,y\ncmp y,#104\nbne !AfterIf15\nbeq !doIf15\n*= !doIf15\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf15\nmov !key,y\ncmp y,#106\nbne !AfterIf16\nbeq !doIf16\n*= !doIf16\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf16\nmov !key,y\ncmp y,#107\nbne !AfterIf17\nbeq !doIf17\n*= !doIf17\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf17\nmov !key,y\ncmp y,#108\nbne !AfterIf18\nbeq !doIf18\n*= !doIf18\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf18\nmov !key,y\ncmp y,#122\nbne !AfterIf19\nbeq !doIf19\n*= !doIf19\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf19\nmov !key,y\ncmp y,#120\nbne !AfterIf20\nbeq !doIf20\n*= !doIf20\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf20\nmov !key,y\ncmp y,#99\nbne !AfterIf21\nbeq !doIf21\n*= !doIf21\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf21\nmov !key,y\ncmp y,#118\nbne !AfterIf22\nbeq !doIf22\n*= !doIf22\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf22\nmov !key,y\ncmp y,#98\nbne !AfterIf23\nbeq !doIf23\n*= !doIf23\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf23\nmov !key,y\ncmp y,#110\nbne !AfterIf24\nbeq !doIf24\n*= !doIf24\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf24\nmov !key,y\ncmp y,#109\nbne !AfterIf25\nbeq !doIf25\n*= !doIf25\nmov $524287,x\nmov x,!keyPress\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf25\nmov !key,y\ncmp y,#96\nbne !AfterIf26\nbeq !doIf26\n*= !doIf26\nmov !keyCount,x\nmov #1,y\nsub x,y\n mov y,!keyCount\nmov #0,x\nmov x,$524287\njsr !cacheKey\n*= !AfterIf26\nmov !key,y\ncmp y,#124\nbne !AfterIf27\nbeq !doIf27\n*= !doIf27\n")
                for x in range(len(fullLine)):
                    if fullLine[x] == "if":
                        next
                    elif fullLine[x] == "input":
                        next
                    elif fullLine[x] == "=":
                        next
                    else:
                        print(fullLine[x])
                        new_string = new_string + fullLine[x] + " "
                    print(new_string)
                    new_string = new_string.split()
                asm.write("den\n")
                asm.write("*= !AfterIf27\ndcs \nmov !keyPress,x \ndra x \njsr !inputLoop\nrts\n*= !cacheKey\nmov !keyCount,y\ncmp y,#0\nbne !AfterIf28\nbeq !doIf28\n*= !doIf28\nmov !keyPress,x\nmov x,!word0\n*= !AfterIf28\nmov !keyCount,y\ncmp y,#1\nbne !AfterIf29\nbeq !doIf29\n*= !doIf29\nmov !keyPress,x\nmov x,!word1\n*= !AfterIf29\nmov !keyCount,y\ncmp y,#2\nbne !AfterIf30\nbeq !doIf30\n*= !doIf30\nmov !keyPress,x\nmov x,!word2\n*= !AfterIf30\nmov !keyCount,y\ncmp y,#3\nbne !AfterIf31\nbeq !doIf31\n*= !doIf31\nmov !keyPress,x\nmov x,!word3\n*= !AfterIf31\nmov !keyCount,y\ncmp y,#4\nbne !AfterIf32\nbeq !doIf32\n*= !doIf32\nmov !keyPress,x\nmov x,!word4\n*= !AfterIf32\nmov !keyCount,y\ncmp y,#5\nbne !AfterIf33\nbeq !doIf33\n*= !doIf33\nmov !keyPress,x\nmov x,!word5\n*= !AfterIf33\nmov !keyCount,y\ncmp y,#6\nbne !AfterIf34\nbeq !doIf34\n*= !doIf34\nmov !keyPress,x\nmov x,!word6\n*= !AfterIf34\nmov !keyCount,y\ncmp y,#7\nbne !AfterIf35\nbeq !doIf35\n*= !doIf35\nmov !keyPress,x\nmov x,!word7\n*= !AfterIf35\nmov !keyCount,y\ncmp y,#8\nbne !AfterIf36\nbeq !doIf36\n*= !doIf36\nmov !keyPress,x\nmov x,!word8\n*= !AfterIf36\nmov !keyCount,y\ncmp y,#9\nbne !AfterIf37\nbeq !doIf37\n*= !doIf37\nmov !keyPress,x\nmov x,!word9\n*= !AfterIf37\nmov !keyCount,y\ncmp y,#10\nbne !AfterIf38\nbeq !doIf38\n*= !doIf38\nmov !keyPress,x\nmov x,!word10\n*= !AfterIf38\nmov !keyCount,y\ncmp y,#11\nbne !AfterIf39\nbeq !doIf39\n*= !doIf39\nmov !keyPress,x\nmov x,!word11\n*= !AfterIf39\nmov !keyCount,y\ncmp y,#12\nbne !AfterIf40\nbeq !doIf40\n*= !doIf40\nmov !keyPress,x\nmov x,!word12\n*= !AfterIf40\nmov !keyCount,y\ncmp y,#13\nbne !AfterIf41\nbeq !doIf41\n*= !doIf41\nmov !keyPress,x\nmov x,!word13\n*= !AfterIf41\nmov !keyCount,y\ncmp y,#14\nbne !AfterIf42\nbeq !doIf42\n*= !doIf42\nmov !keyPress,x\nmov x,!word14\n*= !AfterIf42\nmov !keyCount,y\ncmp y,#15\nbne !AfterIf43\nbeq !doIf43\n*= !doIf43\nmov !keyPress,x\nmov x,!word15\n*= !AfterIf43\nmov !keyCount,y\ncmp y,#16\nbne !AfterIf44\nbeq !doIf44\n*= !doIf44\nmov !keyPress,x\nmov x,!word16\n*= !AfterIf44\nmov !keyCount,y\ncmp y,#17\nbne !AfterIf45\nbeq !doIf45\n*= !doIf45\nmov !keyPress,x\nmov x,!word17\n*= !AfterIf45\nmov !keyCount,y\ncmp y,#18\nbne !AfterIf46\nbeq !doIf46\n*= !doIf46\nmov !keyPress,x\nmov x,!word18\n*= !AfterIf46\nmov !keyCount,y\ncmp y,#19\nbne !AfterIf47\nbeq !doIf47\n*= !doIf47\nmov !keyPress,x\nmov x,!word19\n*= !AfterIf47\nmov !keyCount,y\ncmp y,#20\nbne !AfterIf48\nbeq !doIf48\n*= !doIf48\nmov !keyPress,x\nmov x,!word20\n*= !AfterIf48\nmov !keyCount,y\ncmp y,#21\nbne !AfterIf49\nbeq !doIf49\n*= !doIf49\nmov !keyPress,x\nmov x,!word21\n*= !AfterIf49\nmov !keyCount,y\ncmp y,#22\nbne !AfterIf50\nbeq !doIf50\n*= !doIf50\nmov !keyPress,x\nmov x,!word22\n*= !AfterIf50\nmov !keyCount,y\ncmp y,#23\nbne !AfterIf51\nbeq !doIf51\n*= !doIf51\nmov !keyPress,x\nmov x,!word23\n*= !AfterIf51\nmov !keyCount,y\ncmp y,#24\nbne !AfterIf52\nbeq !doIf52\n*= !doIf52\nmov !keyPress,x\nmov x,!word24\n*= !AfterIf52\nmov !keyCount,y\ncmp y,#25\nbne !AfterIf53\nbeq !doIf53\n*= !doIf53\nmov !keyPress,x\nmov x,!word25\n*= !AfterIf53\nmov !keyCount,y\ncmp y,#26\nbne !AfterIf54\nbeq !doIf54\n*= !doIf54\nmov !keyPress,x\nmov x,!word26\n*= !AfterIf54\nmov !keyCount,y\ncmp y,#27\nbne !AfterIf55\nbeq !doIf55\n*= !doIf55\nmov !keyPress,x\nmov x,!word27\n*= !AfterIf55\nmov !keyCount,y\ncmp y,#28\nbne !AfterIf56\nbeq !doIf56\n*= !doIf56\nmov !keyPress,x\nmov x,!word28\n*= !AfterIf56\nmov !keyCount,y\ncmp y,#29\nbne !AfterIf57\nbeq !doIf57\n*= !doIf57\nmov !keyPress,x\nmov x,!word29\n*= !AfterIf57\nmov !keyCount,y\ncmp y,#30\nbne !AfterIf58\nbeq !doIf58\n*= !doIf58\nmov !keyPress,x\nmov x,!word30\n*= !AfterIf58\nmov !keyCount,y\ncmp y,#31\nbne !AfterIf59\nbeq !doIf59\n*= !doIf59\nmov !keyPress,x\nmov x,!word31\n*= !AfterIf59\nmov !keyCount,y\ncmp y,#32\nbne !AfterIf60\nbeq !doIf60\n*= !doIf60\nmov !keyPress,x\nmov x,!word32\n*= !AfterIf60\nmov !keyCount,y\ncmp y,#33\nbne !AfterIf61\nbeq !doIf61\n*= !doIf61\nmov !keyPress,x\nmov x,!word33\n*= !AfterIf61\nmov !keyCount,y\ncmp y,#34\nbne !AfterIf62\nbeq !doIf62\n*= !doIf62\nmov !keyPress,x\nmov x,!word34\n*= !AfterIf62\nmov !keyCount,y\ncmp y,#35\nbne !AfterIf63\nbeq !doIf63\n*= !doIf63\nmov !keyPress,x\nmov x,!word35\n*= !AfterIf63\nmov !keyCount,y\ncmp y,#36\nbne !AfterIf64\nbeq !doIf64\n*= !doIf64\nmov !keyPress,x\nmov x,!word36\n*= !AfterIf64\nmov !keyCount,y\ncmp y,#37\nbne !AfterIf65\nbeq !doIf65\n*= !doIf65\nmov !keyPress,x\nmov x,!word37\n*= !AfterIf65\nmov !keyCount,y\ncmp y,#38\nbne !AfterIf66\nbeq !doIf66\n*= !doIf66\nmov !keyPress,x\nmov x,!word38\n*= !AfterIf66\nmov !keyCount,y\ncmp y,#39\nbne !AfterIf67\nbeq !doIf67\n*= !doIf67\nmov !keyPress,x\nmov x,!word39\n*= !AfterIf67\nmov !keyCount,x\nmov #1,y\nadd x,y\n mov y,!keyCount\nmov !keyCount,y\ncmp y,#40\nbne !AfterIf68\nbeq !doIf68\n*= !doIf68\n*= !AfterIf68\nrts\n.var key *\n.var keyPress *\n.var keyCount *\n.var word0 *\n.var word1 *\n.var word2 *\n.var word3 *\n.var word4 *\n.var word5 *\n.var word6 *\n.var word7 *\
                n.var word8 *\n.var word9 *\n.var word10 *\n.var word11 *\n.var word12 *\n.var word13 *\n.var word14 *\n.var word15 *\n.var word16 *\n.var word17 *\n.var word18 *\n.var word19 *\n.var word20 *\n.var word21 *\n.var word22 *\n.var word23 *\n.var word24 *\n.var word25 *\n.var word26 *\n.var word27 *\n.var word28 *\n.var word29 *\n.var word30 *\n.var word31 *\n.var word32 *\n.var word33 *\n.var word34 *\n.var word35 *\n.var word36 *\n.var word37 *\n.var word38 *\n.var word39 * \n")
        
            
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
                asm.write("mov #"+str(von)+",x\n")
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

asm.write("return 0"),asm.close(),system('python3 assembler.py')

