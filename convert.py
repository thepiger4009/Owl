from linecache import getline
from pickletools import string4
lc = 1
out = open("ran.txt","w+")
while 1:
    line = getline("asm.txt",lc).rstrip("\n")
    if line == "return 0":
        break
    out.write(line+"/n")
    lc+=1
out.close()
    