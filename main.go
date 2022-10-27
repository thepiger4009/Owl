//main.go
/*
Hawk (Hope all will know)
Build:  1.0.7
Date:   10-26-22
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
var stack [256]uint32     // 256 Byte 32-bit Stack Array

// Registers
var rx, ry, rt, rp, ru uint32 // 32-bit General & Accumulative Registers
var ir uint8                  // 8-bit Instruction Register

// Pointers
var pc uint32 = 256 //Program Counter
var sp uint8        //Stack Pointer

// Flags
var ef, mf, inf, hei byte // Equal flag, Math Flag, Interrupt Flag

// Emulation Flags
var debugDisplay byte = 0
var cycles int = 0 //Used every now and then.
var debugLast byte = 0

// Execution Cycle of Hawk Core
func cycle() {
	getInstruction()
	decodeInstruction()
}

// Setup certain aspects of the Hawk
func setup() {
	loadRom()          // Load contents of rom.txt into Memory
	memory[524287] = 1 // Set keyboard address to 1

	// Keyboard Check function, sets address 65000 in emulation memory to value of keyboard in ascii
	go func() {
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

	// SPE_ Internal Timer Chip
	go func() {
		for {
			memory[524286] += 1
			if memory[524286] > 60 {
				memory[524286] = 0
			}
		}
	}()

	//DebugDisplay
	go func() {
		for {
			if debugDisplay == 1 {
				fmt.Print("\033[H\033[2J")
				fmt.Println("RX:", rx, "RY:", ry, "RT:", rt, "RP:", rp, "RU:", ru)
				fmt.Println("PC:", pc, "IR:", ir, "EF:", ef, "MF:", mf, "KB:", memory[524287])
			}
		}
	}()

	EmulationLoop() // Let the emulation go into it's loop
}

// Main Emulation Loop of Emulator
func EmulationLoop() {
	for {
		cycle()
	}
}

// Function Main - First to be called by Golang
func main() {
	fmt.Println("Hawk(Hope All Will Know) Virtual Machine | Version 1.0.7")
	setup()
}

// Hawk Core Decoder
func decodeInstruction() {
	switch ir {
	case 100:
		switch memory[pc+1] {
		case 1:
			rx = memory[pc+2]
		case 2:
			ry = memory[pc+2]
		case 3:
			rt = memory[pc+2]
		case 4:
			rp = memory[pc+2]
		case 5:
			ru = memory[pc+2]
		}
		pc += 3
		//---------------------------
	case 101:
		switch memory[pc+1] {
		case 1:
			rx = memory[memory[pc+2]]
		case 2:
			ry = memory[memory[pc+2]]
		case 3:
			rt = memory[memory[pc+2]]
		case 4:
			rp = memory[memory[pc+2]]
		case 5:
			ru = memory[memory[pc+2]]
		}
		pc += 3
	case 102:
		switch memory[pc+1] {
		case 1:
			rx = memory[memory[pc+2]+rp]
		case 2:
			ry = memory[memory[pc+2]+rp]
		case 3:
			rt = memory[memory[pc+2]+rp]
		case 4:
			rp = memory[memory[pc+2]+rp]
		case 5:
			ru = memory[memory[pc+2]+rp]
		}
		pc += 3
	case 103:
		switch memory[pc+1] {
		case 1:
			rx = memory[memory[pc+2]+ru]
		case 2:
			ry = memory[memory[pc+2]+ru]
		case 3:
			rt = memory[memory[pc+2]+ru]
		case 4:
			rp = memory[memory[pc+2]+ru]
		case 5:
			ru = memory[memory[pc+2]+ru]
		}
		pc += 3
	case 104:
		switch memory[pc+1] {
		case 1:
			memory[memory[pc+2]] = rx
		case 2:
			memory[memory[pc+2]] = ry
		case 3:
			memory[memory[pc+2]] = rt
		case 4:
			memory[memory[pc+2]] = rp
		case 5:
			memory[memory[pc+2]] = ru
		}
		pc += 3
	case 105:
		switch memory[pc+1] {
		case 1:
			memory[memory[pc+2]+rp] = rx
		case 2:
			memory[memory[pc+2]+rp] = ry
		case 3:
			memory[memory[pc+2]+rp] = rt
		case 4:
			memory[memory[pc+2]+rp] = rp
		case 5:
			memory[memory[pc+2]+rp] = ru
		}
		pc += 3
	case 106:
		switch memory[pc+1] {
		case 1:
			memory[memory[pc+2]+ru] = rx
		case 2:
			memory[memory[pc+2]+ru] = ry
		case 3:
			memory[memory[pc+2]+ru] = rt
		case 4:
			memory[memory[pc+2]+ru] = rp
		case 5:
			memory[memory[pc+2]+ru] = ru
		}
		pc += 3
	case 107:
		switch memory[pc+1] {
		case 1:
			rx += 1
		case 2:
			ry += 1
		case 3:
			rt += 1
		case 4:
			rp += 1
		case 5:
			ru += 1
		}
		pc += 2
	case 108:
		switch memory[pc+1] {
		case 1:
			rx -= 1
		case 2:
			ry -= 1
		case 3:
			rt -= 1
		case 4:
			rp -= 1
		case 5:
			ru -= 1
		}
		pc += 2
	case 109:
		switch memory[pc+1] {
		case 1:
			switch memory[pc+2] {
			case 1:
				rx = rx - 0
			case 2:
				ry = rx
			case 3:
				rt = rx
			case 4:
				rp = rx
			case 5:
				ru = rx
			}
			pc += 3
		case 2:
			switch memory[pc+2] {
			case 1:
				rx = ry
			case 2:
				ry = ry - 0
			case 3:
				rt = ry
			case 4:
				rp = ry
			case 5:
				ru = ry
			}
			pc += 3
		case 3:
			switch memory[pc+2] {
			case 1:
				rx = rt
			case 2:
				ry = rt
			case 3:
				rt = rt - 0
			case 4:
				rp = rt
			case 5:
				ru = rt
			}
			pc += 3
		case 4:
			switch memory[pc+2] {
			case 1:
				rx = rp
			case 2:
				ry = rp
			case 3:
				rt = rp
			case 4:
				rp = rp - 0
			case 5:
				ru = rp
			}
			pc += 3
		case 5:
			switch memory[pc+2] {
			case 1:
				rx = ru
			case 2:
				ry = ru
			case 3:
				rt = ru
			case 4:
				rp = ru
			case 5:
				ru = ru - 0
			}
			pc += 3
		}
	case 110:
		pc = memory[pc+1]
	case 111:
		if ef == 1 {
			pc = memory[pc+1]
			ef = 0
		} else {
			pc += 2
		}
	case 112:
		if ef == 0 {
			pc = memory[pc+1]
		} else {
			pc += 2
		}
	case 113:
		switch memory[pc+1] {
		case 1:
			switch memory[pc+2] {
			case 1:
				rx = rx + rx
			case 2:
				ry = ry + rx
			case 3:
				rt = rt + rx
			case 4:
				rp = rp + rx
			case 5:
				ru = ru + rx
			}
			pc += 3
		case 2:
			switch memory[pc+2] {
			case 1:
				rx = rx + ry
			case 2:
				ry = ry + ry
			case 3:
				rt = rt + ry
			case 4:
				rp = rp + ry
			case 5:
				ru = ru + ry
			}
			pc += 3
		case 3:
			switch memory[pc+2] {
			case 1:
				rx = rx + rt
			case 2:
				ry = ry + rt
			case 3:
				rt = rt + rt
			case 4:
				rp = rp + rt
			case 5:
				ru = ru + rt
			}
			pc += 3
		case 4:
			switch memory[pc+2] {
			case 1:
				rx = rx + rp
			case 2:
				ry = ry + rp
			case 3:
				rt = rt + rp
			case 4:
				rp = rp + rp
			case 5:
				ru = ru + rp
			}
			pc += 3
		case 5:
			switch memory[pc+2] {
			case 1:
				rx = rx + ru
			case 2:
				ry = ry + ru
			case 3:
				rt = rt + ru
			case 4:
				rp = rp + ru
			case 5:
				ru = ru + ru
			}
			pc += 3
		}
	case 114:
		switch memory[pc+1] {
		case 1:
			switch memory[pc+2] {
			case 1:
				rx = rx - rx
			case 2:
				ry = ry - rx
			case 3:
				rt = rt - rx
			case 4:
				rp = rp - rx
			case 5:
				ru = ru - rx
			}
			pc += 3
		case 2:
			switch memory[pc+2] {
			case 1:
				rx = rx - ry
			case 2:
				ry = ry - ry
			case 3:
				rt = rt - ry
			case 4:
				rp = rp - ry
			case 5:
				ru = ru - ry
			}
			pc += 3
		case 3:
			switch memory[pc+2] {
			case 1:
				rx = rx - rt
			case 2:
				ry = ry - rt
			case 3:
				rt = rt - rt
			case 4:
				rp = rp - rt
			case 5:
				ru = ru - rt
			}
			pc += 3
		case 4:
			switch memory[pc+2] {
			case 1:
				rx = rx - rp
			case 2:
				ry = ry - rp
			case 3:
				rt = rt - rp
			case 4:
				rp = rp - rp
			case 5:
				ru = ru - rp
			}
			pc += 3
		case 5:
			switch memory[pc+2] {
			case 1:
				rx = rx - ru
			case 2:
				ry = ry - ru
			case 3:
				rt = rt - ru
			case 4:
				rp = rp - ru
			case 5:
				ru = ru - ru
			}
			pc += 3
		}
	case 115:
		switch memory[pc+1] {
		case 1:
			if rx == memory[pc+2] {
				ef = 1
				pc += 3
			} else {
				pc += 3
			}
		case 2:
			if ry == memory[pc+2] {
				ef = 1
				pc += 3
			} else {
				pc += 3
			}
		case 3:
			if rt == memory[pc+2] {
				ef = 1
				pc += 3
			} else {
				pc += 3
			}
		case 4:
			if rp == memory[pc+2] {
				ef = 1
				pc += 3
			} else {
				pc += 3
			}
		case 5:
			if ru == memory[pc+2] {
				ef = 1
				pc += 3
			} else {
				pc += 3
			}
		}
	case 116:
		if memory[pc+1] == 1 {
			ef = 1
			pc += 2
		} else if memory[pc+1] == 0 {
			ef = 0
			pc += 2
		}
	case 117:
		switch memory[pc+1] {
		case 1:
			stack[sp] = rx
			sp += 1
		case 2:
			stack[sp] = ry
			sp += 1
		case 3:
			stack[sp] = rt
			sp += 1
		case 4:
			stack[sp] = rp
		case 5:
			stack[sp] = ru
		}
		pc += 2
	case 118:
		switch memory[pc+1] {
		case 1:
			rx = stack[sp]
		case 2:
			ry = stack[sp]
		case 3:
			rt = stack[sp]
		case 4:
			rp = stack[sp]
		case 5:
			ru = stack[sp]
		}
		pc += 2
	case 119:
		sp += 1
		pc += 1
	case 120:
		sp -= 1
		pc += 1
	case 121:
		hei = 1
		pc += 1
	case 122:
		hei = 0
		pc += 1
	case 123:
		pc += 1
	case 124: //WRITE OUT REGISTER TO DISPLAY
		switch memory[pc+1] {
		case 1:
			fmt.Print(string(rx))
		case 2:
			fmt.Print(string(ry))
		case 3:
			fmt.Print(string(rt))
		case 4:
			fmt.Print(string(rp))
		case 5:
			fmt.Print(string(ru))
		}
		pc += 2
	case 125:
		fmt.Printf("\b \b")
		pc += 1
	case 126:
		stack[sp] = pc + 2
		sp += 1
		pc = memory[pc+1]
	case 127:
		sp -= 1
		pc = stack[sp]
	case 128:
		stack[sp] = pc + 1
		sp += 1
		pc += 1
	case 129:
		switch memory[pc+1] {
		case 1:
			switch memory[pc+2] {
			case 1:
				if rx == rx {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
			case 2:
				if rx == ry {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
			case 3:
				if rx == rt {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
			case 4:
				if rx == rp {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
			case 5:
				if rx == ru {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
			}
		case 2:
			switch memory[pc+2] {
			case 1:
				if ry == rx {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if ry == ry {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if ry == rt {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if ry == rp {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if ry == ru {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
			case 3:
				if rt == rx {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if rt == ry {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
			case 4:
				if rp == rx {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if rp == ry {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if rp == rt {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if rp == rp {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
				if rp == ru {
					ef = 1
					pc += 3
				} else {
					pc += 3
				}
			}

		}
	case 130:
		fmt.Println("")
		pc += 1
	case 131: //write out register without ascii conversion
		switch memory[pc+1] {
		case 1:
			fmt.Print(rx)
		case 2:
			fmt.Print(ry)
		case 3:
			fmt.Print(rt)
		case 4:
			fmt.Print(rp)
		case 5:
			fmt.Print(ru)
		}
		pc += 2
	case 132:
		fmt.Print("\033[H\033[2J")
		pc += 1
	case 133: //Print Nothing, basically a space
		fmt.Print(" ")
		pc += 1
	case 150:
		pc += 2
	}
}

func getInstruction() {
	ir = uint8(memory[pc])
}

func loadRom() {
	fmt.Println("Hawk (Hope all will know) | Rom Loader")
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
	fmt.Println("Hawk (Hope all will know) | Init.")
	time.Sleep(1 * time.Second)
	fmt.Print("\033[H\033[2J")
	f.Close()
}
