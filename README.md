# Big Update!
SPE_ has been renamed to Owl, and it's main goal has been changed.
Owl's new goal is to basically be a programming language like Java but with the feeling of hardware.
An example would be basic on the Commodore 64. With basic you had a programming language but also you had the hardware and could mess with it at any time. That is what Owl will attempt to replicate.
Owl will still contain its emulation aspect and assembly programming. Some new changes are coming from this new goal such as a memory expansion from 64kb to 512kb and registers now being 32-bit.

# Owl Features:
- Five 32-bit General & Accumulative registers
- 512Kb of Memory
- Keyboard support

# Owl Summary
Owl is a new programming language or techincally my own virtual machine that you can program. It's goal is to be a Commodore 64 mixed with modern day programming. It currently supports assembly and its own programming language which will be named soon.

# How to use!
Setting up Owl should hopefully be easy! If not, I will try to make it easier in the future.
1. Download or make sure you are running golang 1.18 or 1.19
2. Download python3.10 or python3.11, older versions may work but the files using python were coded for 3.10 and 3.11 so you may encounter issues.
3. Build or Run main.go by running the command "go run main.go *FILE NAME*" or "go build main.go".
4. Executing a file is easy. Make sure it is utf-8 text like file, like a .txt file and run "main *file.name*" or if haven't built the project just do "go run main.go *file.name*".

# How to use assembler & compiler!
As of right now I don't have much documentation so you'll have to use what ever I leave sometimes in my asm.txt file. If you need more information just look at the assembler.py & compiler.py which contain how to program.

