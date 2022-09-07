#/~asm.py
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

out = open("rom.txt","w+")

import linecache
from pydoc import visiblename
import re

lc = 1
twoL = ""

do1 = True
lastGOTname = ""
lastGOTaddr = 0
addressLength = [0] * 10000
addressName   = [0] * 10000
customAddressName = [0] * 10000
customAddressPos = [0] * 10000
customCount = 0
addCount = 0
variableNameList = [0] * 10000
variableAdList = [0] * 10000
vc = 0 #variable counter

def getAddress(name):
    for x in range(10000):
        if name == addressName[x]:
            break
    xav = x
    return xav

def getVariableAd(name):
    for x in range(10000):
        if name == variableNameList[x]:
            break
    xav = variableAdList[x]
    return xav

def getCustomAd(name):
    for x in range(10000):
        if name == customAddressName[x]:
            print("X:",x)
            xav = x
            return xav
            break
        
lastgotaddress = ""  
vb = 0 #virtual byte count
while 1: #FINALLY DEALING WITH BS, ADDRESS MAKING
    print("[-DEBUG-]: VIRTUAL BYTES IS:",vb,"LINE COUNT:",lc)
    line = linecache.getline("asm.txt",lc).rstrip("\n")
    fullLine = line.split()
    print(fullLine)
    try:
        twoL = fullLine[1].split(","[0])
    except:
        next
    if line == "return 0":
        break
    if fullLine[0] == "*=":
        print(lastGOTaddr,"is",vb,"bytes long")
        addressName[addCount] = lastGOTaddr
        addressLength[addCount] = vb
        addCount+=1
        vb=0
        lastGOTaddr = fullLine[1]
        print(lastGOTaddr)

    if fullLine[0] == ".var":
        name = fullLine[1]
        tai = fullLine[2]
        variableNameList[vc] = name
        variableAdList[vc] = tai
        vc+=1


    if ":" in fullLine[0]:
        try:     
            one = fullLine[0].split(":"[0])
        except:
            next
        name = one[1]
        
        
        print(getAddress(lastGOTaddr))
        pos = addressLength[getAddress(lastGOTaddr)] + int(lastGOTaddr)
        customAddressName[customCount] = name
        customAddressPos[customCount] = pos+vb
        customCount+=1
        print(name,"is at",pos+vb)
        print("[DEBUG]: Trying to get",name,"address!: GOT:",getCustomAd(name))
        vb = 0
        
    if fullLine[0] == "nop":
        vb+=1

    if ":" in fullLine[0]:
        vb+=2

    if fullLine[0] == "sef":
        vb+=2

    if fullLine[0] == "isp":
        vb+=1
    if fullLine[0] == "dsp":
        vb+=1

    if fullLine[0] == "ehi":
        vb+=1
    if fullLine[0] == "dhi":
        vb+=1
    if fullLine[0] == "back":
        vb+=1
    




    if fullLine[0] == "cmp":
        vor1 = twoL[0]
        if vor1 == "x":
            vb+=3
        if vor1 == "y":
            vb+=3
        if vor1 == "t":
            vb+=3
        if vor1 == "p":
            vb+=3
        if vor1 == "u":
            vb+=3

    if fullLine[0] == "inc":
        match fullLine[1]:
            case "x":
                vb+=2
            case "y":
                vb+=2
            case "t":
                vb+=2
            case "p":
                vb+=2
            case "u":
                vb+=2

    if fullLine[0] == "dec":
        match fullLine[1]:
            case "x":
                vb+=2
            case "y":
                vb+=2
            case "t":
                vb+=2
            case "p":
                vb+=2
            case "u":
                vb+=2

    if fullLine[0] == "jmp":
        vb+=2

    if fullLine[0] == "beq":
        vb+=2
    
    if fullLine[0] == "bne":
        vb+=2

    if fullLine[0] == "out":
        reg = fullLine[1]
        if reg == "x":
            vb+=2
        if reg == "y":
            vb+=2
        if reg == "t":
            vb+=2
        if reg == "p":
            vb+=2
        if reg == "u":
            vb+=2

    if fullLine[0] == "jsr":
        vb+=2

    if fullLine[0] == "rts":
        vb+=1

    if fullLine[0] == "add":
        vor1 = twoL[0]
        vor2 = twoL[1]

        if vor1 == "x":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3
        if vor1 == "y":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if vor1 == "t":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if vor1 == "p":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if vor1 == "u":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

    if fullLine[0] == "sub":
        vor1 = twoL[0]
        vor2 = twoL[1]

        if vor1 == "x":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3
        if vor1 == "y":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if vor1 == "t":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if vor1 == "p":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if vor1 == "u":
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3
    if fullLine[0] == "mov":
        vor1 = twoL[0] # Value or Register 1
        vor2 = twoL[1] # Value or Register 2

        if vor1 == "pc":
            if vor2 == "stack":
                vb+=1

        if vor1 == "x":
            if vor2 == "x":
                vb+=3
                do1 = False
            if vor2 == "y":
                vb+=3
                do1 = False
            if vor2 == "t":
                vb+=3
                do1 = False
            if vor2 == "p":
                vb+=3
                do1 = False
            if vor2 == "u":
                vb+=3
                do1 = False

        if vor1 == "y":
            if vor2 == "x":
                vb+=3
                do1 = False
            if vor2 == "y":
                vb+=3
                do1 = False
            if vor2 == "t":
                vb+=3
                do1 = False
            if vor2 == "p":
                vb+=3
                do1 = False
            if vor2 == "u":
                vb+=3
                do1 = False
        
        if vor1 == "t":
            if vor2 == "x":
                vb+=3
                do1 = False
            if vor2 == "y":
                vb+=3
                do1 = False
            if vor2 == "t":
                vb+=3
                do1 = False
            if vor2 == "p":
                vb+=3
                do1 = False
            if vor2 == "u":
                vb+=3
                do1 = False

        if vor1 == "p":
            if vor2 == "x":
                vb+=3
                do1 = False
            if vor2 == "y":
                vb+=3
                do1 = False
            if vor2 == "t":
                vb+=3
                do1 = False
            if vor2 == "p":
                vb+=3
                do1 = False
            if vor2 == "u":
                vb+=3
                do1 = False
  
        if vor1 == "u":
            if vor2 == "x":
                vb+=3
                do1 = False
            if vor2 == "y":
                vb+=3
                do1 = False
            if vor2 == "t":
                vb+=3
                do1 = False
            if vor2 == "p":
                vb+=3
                do1 = False
            if vor2 == "u":
                vb+=3
                do1 = False


        if "$" in vor2:
            if vor1 == "x":
                vb+=3
            if vor1 == "y":
                vb+=3
            if vor1 == "t":
                vb+=3
            if vor1 == "p":
                vb+=3
            if vor1 == "u":
                vb+=3
        
        if "$" in vor1:
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if "#" in vor1:
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if "p%" in vor1:
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if "u%" in vor1:
            if vor2 == "x":
                vb+=3
            if vor2 == "y":
                vb+=3
            if vor2 == "t":
                vb+=3
            if vor2 == "p":
                vb+=3
            if vor2 == "u":
                vb+=3

        if "p%" in vor2:
            if vor1 == "x":
                vb+=3
            if vor1 == "y":
                vb+=3
            if vor1 == "t":
                vb+=3
            if vor1 == "p":
                vb+=3
            if vor1 == "u":
                vb+=3

        if "u%" in vor2:
            if vor1 == "x":
                vb+=3
            if vor1 == "y":
                vb+=3
            if vor1 == "t":
                vb+=3
            if vor1 == "p":
                vb+=3
            if vor1 == "u":
                vb+=3

        if vor2 == "stack":
            vb+=1
            if vor1 == "x":
                vb+=1
            if vor1 == "y":
                vb+=1
            if vor1 == "t":
                vb+=1
            if vor1 == "p":
                vb+=1
            if vor1 == "u":
                vb+=1

        if vor1 == "stack":
            vb+=1
            if vor2 == "x":
                vb+=1
            if vor2 == "y":
                vb+=1
            if vor2 == "t":
                vb+=1
            if vor2 == "p":
                vb+=1
            if vor2 == "u":
                vb+=1

                
    lc+=1

lc = 1
# THIS IS NORMAL DO NOT ADD VB HERE -------------------------------------- 

while True:
    do1 = True
    line = linecache.getline("asm.txt",lc).rstrip("\n")
    if line == "return 0":
        break
    fullLine = line.split()
    try:
        twoL = fullLine[1].split(","[0])
    except:
        next

    if fullLine[0] == "nop":
        out.writelines("123\n")

    if ";" in fullLine[0]:
        next

    if fullLine[0] == "*=":
        lastgotaddress = fullLine[1]
        address = fullLine[1]
        out.writelines("loadAddress\n")
        out.writelines(address)
        out.writelines("\n")


    if fullLine[0] == "sef":
        val = fullLine[1]
        out.writelines("116\n")
        out.writelines(str(val))
        out.writelines("\n")

    if fullLine[0] == "isp":
        out.writelines("119\n")
    if fullLine[0] == "dsp":
        out.writelines("120\n")

    if fullLine[0] == "ehi":
        out.writelines("121\n")
    if fullLine[0] == "dhi":
        out.writelines("122\n")
    
    if fullLine[0] == ".string":
        address = fullLine[1]
        tcc = 2 #TEMP CC
        out.writelines("loadAddress\n")
        out.writelines(str(address))
        out.writelines("\n")
        while 1:
            if fullLine[tcc] == "}":
                break
            
            for x in range(len(fullLine[tcc])):
                out.writelines(str(ord(fullLine[tcc][x])))
                out.writelines("\n")
            out.writelines("32\n")
            tcc+=1

        



    if fullLine[0] == "cmp":
        vor1 = twoL[0]
        vor2 = twoL[1]
        if vor1 == "x":
            if vor2 == "x":
                out.writelines("129\n1\n1\n")
            if vor2 == "y":
                out.writelines("129\n1\n2\n")
            if vor2 == "t":
                out.writelines("129\n1\n3\n")
            if vor2 == "p":
                out.writelines("129\n1\n4\n")
            if vor2 == "u":
                out.writelines("129\n1\n5\n")
        if vor1 == "y":
            if vor2 == "x":
                out.writelines("129\n2\n1\n")
            if vor2 == "y":
                out.writelines("129\n2\n2\n")
            if vor2 == "t":
                out.writelines("129\n2\n3\n")
            if vor2 == "p":
                out.writelines("129\n2\n4\n")
            if vor2 == "u":
                out.writelines("129\n2\n5\n")
        if vor1 == "t":
            if vor2 == "x":
                out.writelines("129\n3\n1\n")
            if vor2 == "y":
                out.writelines("129\n3\n2\n")
            if vor2 == "t":
                out.writelines("129\n3\n3\n")
            if vor2 == "p":
                out.writelines("129\n3\n4\n")
            if vor2 == "u":
                out.writelines("129\n3\n5\n")
        if vor1 == "p":
            if vor2 == "x":
                out.writelines("129\n4\n1\n")
            if vor2 == "y":
                out.writelines("129\n4\n2\n")
            if vor2 == "t":
                out.writelines("129\n4\n3\n")
            if vor2 == "p":
                out.writelines("129\n4\n4\n")
            if vor2 == "u":
                out.writelines("129\n4\n5\n")
        if vor1 == "u":
            if vor2 == "x":
                out.writelines("129\n5\n1\n")
            if vor2 == "y":
                out.writelines("129\n5\n2\n")
            if vor2 == "t":
                out.writelines("129\n5\n3\n")
            if vor2 == "p":
                out.writelines("129\n5\n4\n")
            if vor2 == "u":
                out.writelines("129\n5\n5\n")
        if "#" in vor2:
            if vor1 == "x":
                try:
                    one = vor2.split("#"[0])
                except:
                    next
                out.writelines("115\n1\n")
                out.writelines(str(one[1]))
                out.writelines("\n")
            if vor1 == "y":
                try:
                    one = vor2.split("#"[0])
                except:
                    next
                out.writelines("115\n2\n")
                out.writelines(str(one[1]))
                out.writelines("\n")
            if vor1 == "t":
                try:
                    one = vor2.split("#"[0])
                except:
                    next
                out.writelines("115\n3\n")
                out.writelines(str(one[1]))
                out.writelines("\n")
            if vor1 == "p":
                try:
                    one = vor2.split("#"[0])
                except:
                    next
                out.writelines("115\n4\n")
                out.writelines(str(one[1]))
                out.writelines("\n")
            if vor1 == "u":
                try:
                    one = vor2.split("#"[0])
                except:
                    next
                out.writelines("115\n5\n")
                out.writelines(str(one[1]))
                out.writelines("\n")
                
    if fullLine[0] == "den":
        out.writelines("130\n")

            

    if fullLine[0] == "inc":
        match fullLine[1]:
            case "x":
                out.writelines("107\n1\n")
            case "y":
                out.writelines("107\n2\n")
            case "t":
                out.writelines("107\n3\n")
            case "p":
                out.writelines("107\n4\n")
            case "u":
                out.writelines("107\n5\n")

    if fullLine[0] == "dec":
        match fullLine[1]:
            case "x":
                out.writelines("108\n1\n")
            case "y":
                out.writelines("108\n2\n")
            case "t":
                out.writelines("108\n3\n")
            case "p":
                out.writelines("108\n4\n")
            case "u":
                out.writelines("108\n5\n")

    if fullLine[0] == "jmp":
        if "!" in fullLine[1]:
            try:     
                one = fullLine[1].split("!"[0])
            except:
                next
            address = customAddressPos[getCustomAd(one[1])]
            print("[JMP]: WANTED",one[1],"and got:",address)
            out.writelines("110\n")
            out.writelines(str(address))
            out.writelines("\n")


        else:
            add = fullLine[1]
            out.writelines("110\n")
            out.writelines(str(add))
            out.writelines("\n")
    if fullLine[0] == "psb": #PROCESSOR SOUND BEEP
        out.writelines("133\n")

    if fullLine[0] == "beq":
        if "!" in fullLine[1]:
            try:     
                one = fullLine[1].split("!"[0])
            except:
                next
            address = customAddressPos[getCustomAd(one[1])]
            print("[BEQ]: WANTED",one[1],"and got:",address)
            out.writelines("111\n")
            out.writelines(str(address))
            out.writelines("\n")
        
        else:
            add = fullLine[1]
            out.writelines("111\n")
            out.writelines(str(add))
            out.writelines("\n")
    
    if fullLine[0] == "bne":
        if "!" in fullLine[1]:
            try:     
                one = fullLine[1].split("!"[0])
            except:
                next
            address = customAddressPos[getCustomAd(one[1])]
            print("[BNE]: WANTED",one[1],"and got:",address)
            out.writelines("112\n")
            out.writelines(str(address))
            out.writelines("\n")

        else:

            add = fullLine[1]
            out.writelines("112\n")
            out.writelines(str(add))
            out.writelines("\n")

    if fullLine[0] == "dbk":
        out.writelines("125\n")

    if fullLine[0] == "dcs": # DISPLAY CLEAR SCREEN
        out.writelines("132\n")

    if fullLine[0] == "drv": # Display register value
        reg = fullLine[1]
        if reg == "x":
            out.writelines("131\n1\n")
        if reg == "y":
            out.writelines("131\n2\n")
        if reg == "t":
            out.writelines("131\n3\n")
        if reg == "p":
            out.writelines("131\n4\n")
        if reg == "u":
            out.writelines("131\n5\n")

    if fullLine[0] == "dra": # Display Register in ascii
        reg = fullLine[1]
        if reg == "x":
            out.writelines("124\n1\n")
        if reg == "y":
            out.writelines("124\n2\n")
        if reg == "t":
            out.writelines("124\n3\n")
        if reg == "p":
            out.writelines("124\n4\n")
        if reg == "u":
            out.writelines("124\n5\n")

    if fullLine[0] == "jsr":
        add = fullLine[1]
        out.writelines("126\n")
        out.writelines(str(add))
        out.writelines("\n")

    if fullLine[0] == "rts":
        out.writelines("127\n")

    if fullLine[0] == "add":
        vor1 = twoL[0]
        vor2 = twoL[1]

        if vor1 == "x":
            if vor2 == "x":
                out.writelines("113\n1\n1\n")
            if vor2 == "y":
                out.writelines("113\n1\n2\n")
            if vor2 == "t":
                out.writelines("113\n1\n3\n")
            if vor2 == "p":
                out.writelines("113\n1\n4\n")
            if vor2 == "u":
                out.writelines("113\n1\n5\n")
        if vor1 == "y":
            if vor2 == "x":
                out.writelines("113\n2\n1\n")
            if vor2 == "y":
                out.writelines("113\n2\n2\n")
            if vor2 == "t":
                out.writelines("113\n2\n3\n")
            if vor2 == "p":
                out.writelines("113\n2\n4\n")
            if vor2 == "u":
                out.writelines("113\n2\n5\n")

        if vor1 == "t":
            if vor2 == "x":
                out.writelines("113\n3\n1\n")
            if vor2 == "y":
                out.writelines("113\n3\n2\n")
            if vor2 == "t":
                out.writelines("113\n3\n3\n")
            if vor2 == "p":
                out.writelines("113\n3\n4\n")
            if vor2 == "u":
                out.writelines("113\n3\n5\n")

        if vor1 == "p":
            if vor2 == "x":
                out.writelines("113\n4\n1\n")
            if vor2 == "y":
                out.writelines("113\n4\n2\n")
            if vor2 == "t":
                out.writelines("113\n4\n3\n")
            if vor2 == "p":
                out.writelines("113\n4\n4\n")
            if vor2 == "u":
                out.writelines("113\n4\n5\n")

        if vor1 == "u":
            if vor2 == "x":
                out.writelines("113\n5\n1\n")
            if vor2 == "y":
                out.writelines("113\n5\n2\n")
            if vor2 == "t":
                out.writelines("113\n5\n3\n")
            if vor2 == "p":
                out.writelines("113\n5\n4\n")
            if vor2 == "u":
                out.writelines("113\n5\n5\n")

    if fullLine[0] == "sub":
        vor1 = twoL[0]
        vor2 = twoL[1]

        if vor1 == "x":
            if vor2 == "x":
                out.writelines("114\n1\n1\n")
            if vor2 == "y":
                out.writelines("114\n1\n2\n")
            if vor2 == "t":
                out.writelines("114\n1\n3\n")
            if vor2 == "p":
                out.writelines("114\n1\n4\n")
            if vor2 == "u":
                out.writelines("114\n1\n5\n")
        if vor1 == "y":
            if vor2 == "x":
                out.writelines("114\n2\n1\n")
            if vor2 == "y":
                out.writelines("114\n2\n2\n")
            if vor2 == "t":
                out.writelines("114\n2\n3\n")
            if vor2 == "p":
                out.writelines("114\n2\n4\n")
            if vor2 == "u":
                out.writelines("114\n2\n5\n")

        if vor1 == "t":
            if vor2 == "x":
                out.writelines("114\n3\n1\n")
            if vor2 == "y":
                out.writelines("114\n3\n2\n")
            if vor2 == "t":
                out.writelines("114\n3\n3\n")
            if vor2 == "p":
                out.writelines("114\n3\n4\n")
            if vor2 == "u":
                out.writelines("114\n3\n5\n")

        if vor1 == "p":
            if vor2 == "x":
                out.writelines("114\n4\n1\n")
            if vor2 == "y":
                out.writelines("114\n4\n2\n")
            if vor2 == "t":
                out.writelines("114\n4\n3\n")
            if vor2 == "p":
                out.writelines("114\n4\n4\n")
            if vor2 == "u":
                out.writelines("114\n4\n5\n")

        if vor1 == "u":
            if vor2 == "x":
                out.writelines("114\n5\n1\n")
            if vor2 == "y":
                out.writelines("114\n5\n2\n")
            if vor2 == "t":
                out.writelines("114\n5\n3\n")
            if vor2 == "p":
                out.writelines("114\n5\n4\n")
            if vor2 == "u":
                out.writelines("114\n5\n5\n")
    if fullLine[0] == "mov":
        vor1 = twoL[0] # Value or Register 1
        vor2 = twoL[1] # Value or Register 2

        if vor1 == "pc":
            if vor2 == "stack":
                out.write("128\n")

        if "!" in vor1:
            try:
                vname = vor1.split("!"[0])
            except:
                next
            if vor2 == "x":
                out.writelines("101\n1\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            if vor2 == "y":
                out.writelines("101\n2\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            if vor2 == "t":
                out.writelines("101\n3\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            if vor2 == "p":
                out.writelines("101\n4\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            if vor2 == "u":
                out.writelines("101\n5\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")

        if "!" in vor2:
            try:
                vname = vor2.split("!"[0])
            except:
                next
            if vor1 == "x":
                out.writelines("104\n1\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            if vor1 == "y":
                out.writelines("104\n2\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            if vor1 == "t":
                out.writelines("104\n3\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            if vor1 == "p":
                out.writelines("104\n4\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            if vor1 == "u":
                out.writelines("104\n5\n")
                out.writelines(str(getVariableAd(vname[1])))
                out.writelines("\n")
            



        if vor1 == "x":
            if vor2 == "x":
                out.writelines("109\n1\n1\n")
                do1 = False
            if vor2 == "y":
                out.writelines("109\n1\n2\n")
                do1 = False
            if vor2 == "t":
                out.writelines("109\n1\n3\n")
                do1 = False
            if vor2 == "p":
                out.writelines("109\n1\n4\n")
                do1 = False
            if vor2 == "u":
                out.writelines("109\n1\n5\n")
                do1 = False

        if vor1 == "y":
            if vor2 == "x":
                out.writelines("109\n2\n1\n")
                do1 = False
            if vor2 == "y":
                out.writelines("109\n2\n2\n")
                do1 = False
            if vor2 == "t":
                out.writelines("109\n2\n3\n")
                do1 = False
            if vor2 == "p":
                out.writelines("109\n2\n4\n")
                do1 = False
            if vor2 == "u":
                out.writelines("109\n2\n5\n")
                do1 = False
        
        if vor1 == "t":
            if vor2 == "x":
                out.writelines("109\n3\n1\n")
                do1 = False
            if vor2 == "y":
                out.writelines("109\n3\n2\n")
                do1 = False
            if vor2 == "t":
                out.writelines("109\n3\n3\n")
                do1 = False
            if vor2 == "p":
                out.writelines("109\n3\n4\n")
                do1 = False
            if vor2 == "u":
                out.writelines("109\n3\n5\n")
                do1 = False

        if vor1 == "p":
            if vor2 == "x":
                out.writelines("109\n4\n1\n")
                do1 = False
            if vor2 == "y":
                out.writelines("109\n4\n2\n")
                do1 = False
            if vor2 == "t":
                out.writelines("109\n4\n3\n")
                do1 = False
            if vor2 == "p":
                out.writelines("109\n4\n4\n")
                do1 = False
            if vor2 == "u":
                out.writelines("109\n4\n5\n")
                do1 = False
  
        if vor1 == "u":
            if vor2 == "x":
                out.writelines("109\n5\n1\n")
                do1 = False
            if vor2 == "y":
                out.writelines("109\n5\n2\n")
                do1 = False
            if vor2 == "t":
                out.writelines("109\n5\n3\n")
                do1 = False
            if vor2 == "p":
                out.writelines("109\n5\n4\n")
                do1 = False
            if vor2 == "u":
                out.writelines("109\n5\n5\n")
                do1 = False


        if "$" in vor2:
            if vor1 == "x":
                out.writelines("104\n1\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "y":
                out.writelines("104\n2\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "t":
                out.writelines("104\n3\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "p":
                out.writelines("104\n4\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "u":
                out.writelines("104\n5\n")
                print(''.join(x for x in vor1 if x.isdigit()))
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
        
        if "$" in vor1:
            if vor2 == "x":
                out.writelines("101\n1\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "y":
                out.writelines("101\n2\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "t":
                out.writelines("101\n3\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "p":
                out.writelines("101\n4\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "u":
                out.writelines("101\n5\n")
                print(''.join(x for x in vor1 if x.isdigit()))
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")

        if "#" in vor1:
            if vor2 == "x":
                out.writelines("100\n1\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "y":
                out.writelines("100\n2\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "t":
                out.writelines("100\n3\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "p":
                out.writelines("100\n4\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "u":
                out.writelines("100\n5\n")
                print(''.join(x for x in vor1 if x.isdigit()))
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")

        if "p%" in vor1:
            if vor2 == "x":
                out.writelines("102\n1\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "y":
                out.writelines("102\n2\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "t":
                out.writelines("102\n3\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "p":
                out.writelines("102\n4\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "u":
                out.writelines("102\n5\n")
                print(''.join(x for x in vor1 if x.isdigit()))
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")

        if "u%" in vor1:
            if vor2 == "x":
                out.writelines("103\n1\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "y":
                out.writelines("103\n2\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "t":
                out.writelines("103\n3\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "p":
                out.writelines("103\n4\n")
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")
            if vor2 == "u":
                out.writelines("103\n5\n")
                print(''.join(x for x in vor1 if x.isdigit()))
                out.writelines(''.join(x for x in vor1 if x.isdigit()))
                out.writelines("\n")

        if "p%" in vor2:
            if vor1 == "x":
                out.writelines("105\n1\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "y":
                out.writelines("105\n2\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "t":
                out.writelines("105\n3\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "p":
                out.writelines("105\n4\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "u":
                out.writelines("105\n5\n")
                print(''.join(x for x in vor2 if x.isdigit()))
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")

        if "u%" in vor2:
            if vor1 == "x":
                out.writelines("106\n1\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "y":
                out.writelines("106\n2\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "t":
                out.writelines("106\n3\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "p":
                out.writelines("106\n4\n")
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")
            if vor1 == "u":
                out.writelines("106\n5\n")
                print(''.join(x for x in vor2 if x.isdigit()))
                out.writelines(''.join(x for x in vor2 if x.isdigit()))
                out.writelines("\n")

        if vor2 == "stack":
            out.writelines("117\n")
            if vor1 == "x":
                out.writelines("1\n")
            if vor1 == "y":
                out.writelines("2\n")
            if vor1 == "t":
                out.writelines("3\n")
            if vor1 == "p":
                out.writelines("4\n")
            if vor1 == "u":
                out.writelines("5\n")

        if vor1 == "stack":
            out.writelines("118\n")
            if vor2 == "x":
                out.writelines("1\n")
            if vor2 == "y":
                out.writelines("2\n")
            if vor2 == "t":
                out.writelines("3\n")
            if vor2 == "p":
                out.writelines("4\n")
            if vor2 == "u":
                out.writelines("5\n")


                


    lc+=1
    