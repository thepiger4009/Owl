//main.go
/*
Owl Virtual Machine
Build:  1.1.4
Date:   12-5-22
Author: Landon Smith
----------------------------
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
*/

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/eiannone/keyboard"
)

// Arrays
var memory [524288]uint32 // 512KB 32-bit Memory Array

type core struct { //Core
	x uint32 //X 32-bit register
	y uint32 //Y 32-bit register
	t uint32 //T 32-bit register
	p uint32 //P 32-bit register
	u uint32 //U 32-bit register
	o uint8  //O 8-bit opcode register

	pc uint32 //Program Counter 32-bit
	sp uint8  //Stack Pointer 8-bit

	e byte //Equal Flag
	m byte //Math Flag
	i byte //Interrupt Flag
	h byte //Hardware Interrupt Flag

	stack [256]uint32 //Stack 32-bit

	cycle int //Cycle Counter
}

var cpu1 core //cpu1

// Emulation Flags
var debugDisplay byte = 0
var debugLast byte = 0

func main() { // Function Main - First to be called by Golang
	setup()
}

func setup() { // Setup certain aspects of the Hawk

	loadRom()          // Load rom.bin into Memory
	loadProgram()      // Load contents of rom.txt into Memory
	memory[524287] = 1 // Set keyboard address to 1

	go func() { // Keyboard Check function, sets address 524287 in emulation memory to value of keyboard in ascii
		for {
			char, _, err := keyboard.GetSingleKey()
			if err != nil {
				panic(err)
			}
			memory[524287] = uint32(char)
			if memory[524287] == 92 {
				os.Exit(4)
			}
			if memory[524287] == 95 {
				switch debugDisplay {
				case 1:
					debugDisplay = 0
					fmt.Print("\033[H\033[2J")
				case 0:
					debugDisplay = 1
				}
			}
			if memory[524287] == 0 {
				memory[524287] = 32
			}
		}
	}()

	go func() { // SPE_ Internal Timer Chip
		for {
			memory[524286] += 1
			if memory[524286] > 60 {
				memory[524286] = 0
			}
		}
	}()

	go func() { //DebugDisplay
		for {
			if debugDisplay == 1 {
				fmt.Println("X:", cpu1.x, "Y:", cpu1.y, "T:", cpu1.t, "P:", cpu1.p, "U:", cpu1.u, "TC:", cpu1.cycle)
				fmt.Println("PC:", cpu1.pc, "OP:", cpu1.o, "EF:", cpu1.e, "MF:", cpu1.m, "IF:", cpu1.i, "KEY:", memory[524287])
				fmt.Println("--------------------")
			}
		}
	}()

	EmulationLoop() // Let the emulation go into it's loop
}

func EmulationLoop() { // Main Emulation Loop of Emulator
	for {
		cycle()
	}
}

func cycle() { // Execution Cycle of Owl cpu1
	getOpcode()
	decodeOpcode()
}

func getOpcode() {
	cpu1.o = uint8(memory[cpu1.pc])
	cpu1.cycle += 1
}

func decodeOpcode() { // Owl Core Opcode Decode
	cpu1.cycle += 1
	switch cpu1.o {
	case 0:
		cpu1.x = memory[cpu1.pc-2]
		cpu1.y = memory[cpu1.pc-1]
		cpu1.t = memory[cpu1.pc]
		cpu1.p = memory[cpu1.pc+1]
		cpu1.u = memory[cpu1.pc+2]
	case 100:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.x = memory[cpu1.pc+2]
		case 2:
			cpu1.y = memory[cpu1.pc+2]
		case 3:
			cpu1.t = memory[cpu1.pc+2]
		case 4:
			cpu1.p = memory[cpu1.pc+2]
		case 5:
			cpu1.u = memory[cpu1.pc+2]
		}
		cpu1.pc += 3
		//---------------------------
	case 101:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.x = memory[memory[cpu1.pc+2]]
		case 2:
			cpu1.y = memory[memory[cpu1.pc+2]]
		case 3:
			cpu1.t = memory[memory[cpu1.pc+2]]
		case 4:
			cpu1.p = memory[memory[cpu1.pc+2]]
		case 5:
			cpu1.u = memory[memory[cpu1.pc+2]]
		}
		cpu1.pc += 3
	case 102:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.x = memory[memory[cpu1.pc+2]+cpu1.p]
		case 2:
			cpu1.y = memory[memory[cpu1.pc+2]+cpu1.p]
		case 3:
			cpu1.t = memory[memory[cpu1.pc+2]+cpu1.p]
		case 4:
			cpu1.p = memory[memory[cpu1.pc+2]+cpu1.p]
		case 5:
			cpu1.u = memory[memory[cpu1.pc+2]+cpu1.p]
		}
		cpu1.pc += 3
	case 103:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.x = memory[memory[cpu1.pc+2]+cpu1.u]
		case 2:
			cpu1.y = memory[memory[cpu1.pc+2]+cpu1.u]
		case 3:
			cpu1.t = memory[memory[cpu1.pc+2]+cpu1.u]
		case 4:
			cpu1.p = memory[memory[cpu1.pc+2]+cpu1.u]
		case 5:
			cpu1.u = memory[memory[cpu1.pc+2]+cpu1.u]
		}
		cpu1.pc += 3
	case 104:
		switch memory[cpu1.pc+1] {
		case 1:
			memory[memory[cpu1.pc+2]] = cpu1.x
		case 2:
			memory[memory[cpu1.pc+2]] = cpu1.y
		case 3:
			memory[memory[cpu1.pc+2]] = cpu1.t
		case 4:
			memory[memory[cpu1.pc+2]] = cpu1.p
		case 5:
			memory[memory[cpu1.pc+2]] = cpu1.u
		}
		cpu1.pc += 3
	case 105:
		switch memory[cpu1.pc+1] {
		case 1:
			memory[memory[cpu1.pc+2]+cpu1.p] = cpu1.x
		case 2:
			memory[memory[cpu1.pc+2]+cpu1.p] = cpu1.y
		case 3:
			memory[memory[cpu1.pc+2]+cpu1.p] = cpu1.t
		case 4:
			memory[memory[cpu1.pc+2]+cpu1.p] = cpu1.p
		case 5:
			memory[memory[cpu1.pc+2]+cpu1.p] = cpu1.u
		}
		cpu1.pc += 3
	case 106:
		switch memory[cpu1.pc+1] {
		case 1:
			memory[memory[cpu1.pc+2]+cpu1.u] = cpu1.x
		case 2:
			memory[memory[cpu1.pc+2]+cpu1.u] = cpu1.y
		case 3:
			memory[memory[cpu1.pc+2]+cpu1.u] = cpu1.t
		case 4:
			memory[memory[cpu1.pc+2]+cpu1.u] = cpu1.p
		case 5:
			memory[memory[cpu1.pc+2]+cpu1.u] = cpu1.u
		}
		cpu1.pc += 3
	case 107:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.x += 1
		case 2:
			cpu1.y += 1
		case 3:
			cpu1.t += 1
		case 4:
			cpu1.p += 1
		case 5:
			cpu1.u += 1
		}
		cpu1.pc += 2
	case 108:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.x -= 1
		case 2:
			cpu1.y -= 1
		case 3:
			cpu1.t -= 1
		case 4:
			cpu1.p -= 1
		case 5:
			cpu1.u -= 1
		}
		cpu1.pc += 2
	case 109:
		switch memory[cpu1.pc+1] {
		case 1:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x - 0
			case 2:
				cpu1.y = cpu1.x
			case 3:
				cpu1.t = cpu1.x
			case 4:
				cpu1.p = cpu1.x
			case 5:
				cpu1.u = cpu1.x
			}
			cpu1.pc += 3
		case 2:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.y
			case 2:
				cpu1.y = cpu1.y - 0
			case 3:
				cpu1.t = cpu1.y
			case 4:
				cpu1.p = cpu1.y
			case 5:
				cpu1.u = cpu1.y
			}
			cpu1.pc += 3
		case 3:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.t
			case 2:
				cpu1.y = cpu1.t
			case 3:
				cpu1.t = cpu1.t - 0
			case 4:
				cpu1.p = cpu1.t
			case 5:
				cpu1.u = cpu1.t
			}
			cpu1.pc += 3
		case 4:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.p
			case 2:
				cpu1.y = cpu1.p
			case 3:
				cpu1.t = cpu1.p
			case 4:
				cpu1.p = cpu1.p - 0
			case 5:
				cpu1.u = cpu1.p
			}
			cpu1.pc += 3
		case 5:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.u
			case 2:
				cpu1.y = cpu1.u
			case 3:
				cpu1.t = cpu1.u
			case 4:
				cpu1.p = cpu1.u
			case 5:
				cpu1.u = cpu1.u - 0
			}
			cpu1.pc += 3
		}
	case 110:
		cpu1.pc = memory[cpu1.pc+1]
	case 111:
		if cpu1.e == 1 {
			cpu1.pc = memory[cpu1.pc+1]
			cpu1.e = 0
		} else {
			cpu1.pc += 2
		}
	case 112:
		if cpu1.e == 0 {
			cpu1.pc = memory[cpu1.pc+1]
		} else {
			cpu1.pc += 2
		}
	case 113:
		switch memory[cpu1.pc+1] {
		case 1:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x + cpu1.x
			case 2:
				cpu1.y = cpu1.y + cpu1.x
			case 3:
				cpu1.t = cpu1.t + cpu1.x
			case 4:
				cpu1.p = cpu1.p + cpu1.x
			case 5:
				cpu1.u = cpu1.u + cpu1.x
			}
			cpu1.pc += 3
		case 2:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x + cpu1.y
			case 2:
				cpu1.y = cpu1.y + cpu1.y
			case 3:
				cpu1.t = cpu1.t + cpu1.y
			case 4:
				cpu1.p = cpu1.p + cpu1.y
			case 5:
				cpu1.u = cpu1.u + cpu1.y
			}
			cpu1.pc += 3
		case 3:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x + cpu1.t
			case 2:
				cpu1.y = cpu1.y + cpu1.t
			case 3:
				cpu1.t = cpu1.t + cpu1.t
			case 4:
				cpu1.p = cpu1.p + cpu1.t
			case 5:
				cpu1.u = cpu1.u + cpu1.t
			}
			cpu1.pc += 3
		case 4:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x + cpu1.p
			case 2:
				cpu1.y = cpu1.y + cpu1.p
			case 3:
				cpu1.t = cpu1.t + cpu1.p
			case 4:
				cpu1.p = cpu1.p + cpu1.p
			case 5:
				cpu1.u = cpu1.u + cpu1.p
			}
			cpu1.pc += 3
		case 5:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x + cpu1.u
			case 2:
				cpu1.y = cpu1.y + cpu1.u
			case 3:
				cpu1.t = cpu1.t + cpu1.u
			case 4:
				cpu1.p = cpu1.p + cpu1.u
			case 5:
				cpu1.u = cpu1.u + cpu1.u
			}
			cpu1.pc += 3
		}
	case 114:
		switch memory[cpu1.pc+1] {
		case 1:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x - cpu1.x
			case 2:
				cpu1.y = cpu1.y - cpu1.x
			case 3:
				cpu1.t = cpu1.t - cpu1.x
			case 4:
				cpu1.p = cpu1.p - cpu1.x
			case 5:
				cpu1.u = cpu1.u - cpu1.x
			}
			cpu1.pc += 3
		case 2:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x - cpu1.y
			case 2:
				cpu1.y = cpu1.y - cpu1.y
			case 3:
				cpu1.t = cpu1.t - cpu1.y
			case 4:
				cpu1.p = cpu1.p - cpu1.y
			case 5:
				cpu1.u = cpu1.u - cpu1.y
			}
			cpu1.pc += 3
		case 3:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x - cpu1.t
			case 2:
				cpu1.y = cpu1.y - cpu1.t
			case 3:
				cpu1.t = cpu1.t - cpu1.t
			case 4:
				cpu1.p = cpu1.p - cpu1.t
			case 5:
				cpu1.u = cpu1.u - cpu1.t
			}
			cpu1.pc += 3
		case 4:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x - cpu1.p
			case 2:
				cpu1.y = cpu1.y - cpu1.p
			case 3:
				cpu1.t = cpu1.t - cpu1.p
			case 4:
				cpu1.p = cpu1.p - cpu1.p
			case 5:
				cpu1.u = cpu1.u - cpu1.p
			}
			cpu1.pc += 3
		case 5:
			switch memory[cpu1.pc+2] {
			case 1:
				cpu1.x = cpu1.x - cpu1.u
			case 2:
				cpu1.y = cpu1.y - cpu1.u
			case 3:
				cpu1.t = cpu1.t - cpu1.u
			case 4:
				cpu1.p = cpu1.p - cpu1.u
			case 5:
				cpu1.u = cpu1.u - cpu1.u
			}
			cpu1.pc += 3
		}
	case 115:
		switch memory[cpu1.pc+1] {
		case 1:
			if cpu1.x == memory[cpu1.pc+2] {
				cpu1.e = 1
				cpu1.pc += 3
			} else {
				cpu1.pc += 3
			}
		case 2:
			if cpu1.y == memory[cpu1.pc+2] {
				cpu1.e = 1
				cpu1.pc += 3
			} else {
				cpu1.pc += 3
			}
		case 3:
			if cpu1.t == memory[cpu1.pc+2] {
				cpu1.e = 1
				cpu1.pc += 3
			} else {
				cpu1.pc += 3
			}
		case 4:
			if cpu1.p == memory[cpu1.pc+2] {
				cpu1.e = 1
				cpu1.pc += 3
			} else {
				cpu1.pc += 3
			}
		case 5:
			if cpu1.u == memory[cpu1.pc+2] {
				cpu1.e = 1
				cpu1.pc += 3
			} else {
				cpu1.pc += 3
			}
		}
	case 116:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.e = 1
			cpu1.pc += 2
		case 0:
			cpu1.e = 0
			cpu1.pc += 2
		}
	case 117:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.stack[cpu1.sp] = cpu1.x
			cpu1.sp += 1
		case 2:
			cpu1.stack[cpu1.sp] = cpu1.y
			cpu1.sp += 1
		case 3:
			cpu1.stack[cpu1.sp] = cpu1.t
			cpu1.sp += 1
		case 4:
			cpu1.stack[cpu1.sp] = cpu1.p
		case 5:
			cpu1.stack[cpu1.sp] = cpu1.u
		}
		cpu1.pc += 2
	case 118:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.x = cpu1.stack[cpu1.sp]
		case 2:
			cpu1.y = cpu1.stack[cpu1.sp]
		case 3:
			cpu1.t = cpu1.stack[cpu1.sp]
		case 4:
			cpu1.p = cpu1.stack[cpu1.sp]
		case 5:
			cpu1.u = cpu1.stack[cpu1.sp]
		}
		cpu1.pc += 2
	case 119:
		cpu1.sp += 1
		cpu1.pc += 1
	case 120:
		cpu1.sp -= 1
		cpu1.pc += 1
	case 121:
		switch memory[cpu1.pc+1] {
		case 1:
			cpu1.h = 1
			cpu1.pc += 2
		case 0:
			cpu1.h = 0
			cpu1.pc += 2
		}
	case 123:
		cpu1.pc += 1
	case 124: //WRITE OUT REGISTER TO DISPLAY
		switch memory[cpu1.pc+1] {
		case 1:
			fmt.Print(string(cpu1.x))
		case 2:
			fmt.Print(string(cpu1.y))
		case 3:
			fmt.Print(string(cpu1.t))
		case 4:
			fmt.Print(string(cpu1.p))
		case 5:
			fmt.Print(string(cpu1.u))
		}
		cpu1.pc += 2
	case 125:
		fmt.Printf("\b \b")
		cpu1.pc += 1
	case 126:
		cpu1.stack[cpu1.sp] = cpu1.pc + 2
		cpu1.sp += 1
		cpu1.pc = memory[cpu1.pc+1]
	case 127:
		cpu1.sp -= 1
		cpu1.pc = cpu1.stack[cpu1.sp]
	case 128:
		cpu1.stack[cpu1.sp] = cpu1.pc + 1
		cpu1.sp += 1
		cpu1.pc += 1
	case 129:
		switch memory[cpu1.pc+1] {
		case 1:
			switch memory[cpu1.pc+2] {
			case 1:
				if cpu1.x == cpu1.x {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
			case 2:
				if cpu1.x == cpu1.y {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
			case 3:
				if cpu1.x == cpu1.t {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
			case 4:
				if cpu1.x == cpu1.p {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
			case 5:
				if cpu1.x == cpu1.u {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
			}
		case 2:
			switch memory[cpu1.pc+2] {
			case 1:
				if cpu1.y == cpu1.x {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.y == cpu1.y {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.y == cpu1.t {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.y == cpu1.p {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.y == cpu1.u {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
			case 3:
				if cpu1.t == cpu1.x {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.t == cpu1.y {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
			case 4:
				if cpu1.p == cpu1.x {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.p == cpu1.y {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.p == cpu1.t {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.p == cpu1.p {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
				if cpu1.p == cpu1.u {
					cpu1.e = 1
					cpu1.pc += 3
				} else {
					cpu1.pc += 3
				}
			}
		}
	case 130:
		fmt.Println("")
		cpu1.pc += 1
	case 131: //write out register without ascii conversion
		switch memory[cpu1.pc+1] {
		case 1:
			fmt.Print(cpu1.x)
		case 2:
			fmt.Print(cpu1.y)
		case 3:
			fmt.Print(cpu1.t)
		case 4:
			fmt.Print(cpu1.p)
		case 5:
			fmt.Print(cpu1.u)
		}
		cpu1.pc += 2
	case 132:
		fmt.Print("\033[H\033[2J")
		cpu1.pc += 1
	case 133: //Print Nothing, basically a space
		fmt.Print(" ")
		cpu1.pc += 1
	}
}

func loadProgram() {
	fmt.Println("Owl | Rom Loader")
	var count int = 0 //Memory Counter, place line at this memory address

	//Thanks to stackoverflow and some other golang education website, Still don't understand this
	file := os.Args[1:]
	ffile := strings.Join(file, " ")
	f, err := os.Open(ffile)
	if err != nil {
		log.Fatal(err)
	}
	//----

	//Get a line
	scanner := bufio.NewScanner(f)

	//Read file and then store it at appropriate memory address
	for scanner.Scan() {
		line := scanner.Text()
		if line == "loadAddress" {
			scanner.Scan()
			line := scanner.Text()
			linec, _ := strconv.Atoi(line)
			count = linec
			fmt.Println("Setting as", linec, "| Set!:", count)

		} else {
			line2, _ := strconv.Atoi(line)
			memory[count] = uint32(line2)
			fmt.Println("Writing *", line2, "* | Written:", memory[count], "*, | Moving onto next", count+1)
			count += 1
		}
	}
	fmt.Println("Owl | Init.")
	time.Sleep(1 * time.Second)
	fmt.Print("\033[H\033[2J")
	f.Close()
}

func loadRom() {
	fmt.Println("Owl | Rom Loader")
	var count int = 0 //Memory Counter, place line at this memory address

	//Thanks to stackoverflow and some other golang education website, Still don't understand this
	f, err := os.Open("rom.bin")
	if err != nil {
		log.Fatal(err)
	}
	//----

	//Get a line
	scanner := bufio.NewScanner(f)

	//Read file and then store it at appropriate memory address
	for scanner.Scan() {
		line := scanner.Text()
		if line == "loadAddress" {
			scanner.Scan()
			line := scanner.Text()
			linec, _ := strconv.Atoi(line)
			count = linec
			fmt.Println("Setting as", linec, "| Set!:", count)

		} else {
			line2, _ := strconv.Atoi(line)
			memory[count] = uint32(line2)
			fmt.Println("Writing *", line2, "* | Written:", memory[count], "*, | Moving onto next", count+1)
			count += 1
		}
	}
	fmt.Println("Owl | Init.")
	fmt.Print("\033[H\033[2J")
	f.Close()
}
