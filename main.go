//main.go
/*
Simple Processor Emulation
Build:  1.0.1
Date:   9-14-22
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

//Modules being used
import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/eiannone/keyboard"
)

var memory [65536]uint16
var stack [256]uint16
var rx, ry, rt, rp, ru uint16
var ir, sp uint8
var pc uint16 = 0
var ef, mf uint8
var hei uint8

// 1 - Enable | 0 - Disable
var debugDisplay int = 1

func main() {

	loadRom()
	memory[65000] = 1

	go func() {
		for {
			char, _, err := keyboard.GetSingleKey()
			if err != nil {
				panic(err)
			}
			memory[65000] = uint16(char)
			if memory[65000] == 92 {
				os.Exit(4)
			}
			if memory[65000] == 0 {
				memory[65000] = 32
			}

		}
	}()

	for {
		cycle()
	}
}

func cycle() {
	debugCheck()
	getInstruction()
	decodeInstruction()
}

func decodeInstruction() {
	switch ir {
	case 100:
		switch memory[pc+1] {
		case 1:
			rx = memory[pc+2]
			pc += 3
		case 2:
			ry = memory[pc+2]
			pc += 3
		case 3:
			rt = memory[pc+2]
			pc += 3
		case 4:
			rp = memory[pc+2]
			pc += 3
		case 5:
			ru = memory[pc+2]
			pc += 3
		}
	case 101:
		switch memory[pc+1] {
		case 1:
			rx = memory[memory[pc+2]]
			pc += 3
		case 2:
			ry = memory[memory[pc+2]]
			pc += 3
		case 3:
			rt = memory[memory[pc+2]]
			pc += 3
		case 4:
			rp = memory[memory[pc+2]]
			pc += 3
		case 5:
			ru = memory[memory[pc+2]]
			pc += 3
		}
	case 102:
		switch memory[pc+1] {
		case 1:
			rx = memory[memory[pc+2]+rp]
			pc += 3
		case 2:
			ry = memory[memory[pc+2]+rp]
			pc += 3
		case 3:
			rt = memory[memory[pc+2]+rp]
			pc += 3
		case 4:
			rp = memory[memory[pc+2]+rp]
			pc += 3
		case 5:
			ru = memory[memory[pc+2]+rp]
			pc += 3
		}
	case 103:
		switch memory[pc+1] {
		case 1:
			rx = memory[memory[pc+2]+ru]
			pc += 3
		case 2:
			ry = memory[memory[pc+2]+ru]
			pc += 3
		case 3:
			rt = memory[memory[pc+2]+ru]
			pc += 3
		case 4:
			rp = memory[memory[pc+2]+ru]
			pc += 3
		case 5:
			ru = memory[memory[pc+2]+ru]
			pc += 3
		}
	case 104:
		switch memory[pc+1] {
		case 1:
			memory[memory[pc+2]] = rx
			pc += 3
		case 2:
			memory[memory[pc+2]] = ry
			pc += 3
		case 3:
			memory[memory[pc+2]] = rt
			pc += 3
		case 4:
			memory[memory[pc+2]] = rp
			pc += 3
		case 5:
			memory[memory[pc+2]] = ru
			pc += 3
		}
	case 105:
		switch memory[pc+1] {
		case 1:
			memory[memory[pc+2]+rp] = rx
			pc += 3
		case 2:
			memory[memory[pc+2]+rp] = ry
			pc += 3
		case 3:
			memory[memory[pc+2]+rp] = rt
			pc += 3
		case 4:
			memory[memory[pc+2]+rp] = rp
			pc += 3
		case 5:
			memory[memory[pc+2]+rp] = ru
			pc += 3
		}
	case 106:
		switch memory[pc+1] {
		case 1:
			memory[memory[pc+2]+ru] = rx
			pc += 3
		case 2:
			memory[memory[pc+2]+ru] = ry
			pc += 3
		case 3:
			memory[memory[pc+2]+ru] = rt
			pc += 3
		case 4:
			memory[memory[pc+2]+ru] = rp
			pc += 3
		case 5:
			memory[memory[pc+2]+ru] = ru
			pc += 3
		}
	case 107:
		switch memory[pc+1] {
		case 1:
			rx += 1
			pc += 2
		case 2:
			ry += 1
			pc += 2
		case 3:
			rt += 1
			pc += 2
		case 4:
			rp += 1
			pc += 2
		case 5:
			ru += 1
			pc += 2
		}
	case 108:
		switch memory[pc+1] {
		case 1:
			rx -= 1
			pc += 2
		case 2:
			ry -= 1
			pc += 2
		case 3:
			rt -= 1
			pc += 2
		case 4:
			rp -= 1
			pc += 2
		case 5:
			ru -= 1
			pc += 2
		}
	case 109:
		switch memory[pc+1] {
		case 1:
			switch memory[pc+2] {
			case 1:
				rx = rx - 0
				pc += 3
			case 2:
				ry = rx
				pc += 3
			case 3:
				rt = rx
				pc += 3
			case 4:
				rp = rx
				pc += 3
			case 5:
				ru = rx
				pc += 3
			}
		case 2:
			switch memory[pc+2] {
			case 1:
				rx = ry
				pc += 3
			case 2:
				ry = ry - 0
				pc += 3
			case 3:
				rt = ry
				pc += 3
			case 4:
				rp = ry
				pc += 3
			case 5:
				ru = ry
				pc += 3
			}
		case 3:
			switch memory[pc+2] {
			case 1:
				rx = rt
				pc += 3
			case 2:
				ry = rt
				pc += 3
			case 3:
				rt = rt - 0
				pc += 3
			case 4:
				rp = rt
				pc += 3
			case 5:
				ru = rt
				pc += 3
			}
		case 4:
			switch memory[pc+2] {
			case 1:
				rx = rp
				pc += 3
			case 2:
				ry = rp
				pc += 3
			case 3:
				rt = rp
				pc += 3
			case 4:
				rp = rp - 0
				pc += 3
			case 5:
				ru = rp
				pc += 3
			}
		case 5:
			switch memory[pc+2] {
			case 1:
				rx = ru
				pc += 3
			case 2:
				ry = ru
				pc += 3
			case 3:
				rt = ru
				pc += 3
			case 4:
				rp = ru
				pc += 3
			case 5:
				ru = ru - 0
				pc += 3
			}
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
				pc += 3
			case 2:
				ry = ry + rx
				pc += 3
			case 3:
				rt = rt + rx
				pc += 3
			case 4:
				rp = rp + rx
				pc += 3
			case 5:
				ru = ru + rx
				pc += 3
			}
		case 2:
			switch memory[pc+2] {
			case 1:
				rx = rx + ry
				pc += 3
			case 2:
				ry = ry + ry
				pc += 3
			case 3:
				rt = rt + ry
				pc += 3
			case 4:
				rp = rp + ry
				pc += 3
			case 5:
				ru = ru + ry
				pc += 3
			}
		case 3:
			switch memory[pc+2] {
			case 1:
				rx = rx + rt
				pc += 3
			case 2:
				ry = ry + rt
				pc += 3
			case 3:
				rt = rt + rt
				pc += 3
			case 4:
				rp = rp + rt
				pc += 3
			case 5:
				ru = ru + rt
				pc += 3
			}
		case 4:
			switch memory[pc+2] {
			case 1:
				rx = rx + rp
				pc += 3
			case 2:
				ry = ry + rp
				pc += 3
			case 3:
				rt = rt + rp
				pc += 3
			case 4:
				rp = rp + rp
				pc += 3
			case 5:
				ru = ru + rp
				pc += 3
			}
		case 5:
			switch memory[pc+2] {
			case 1:
				rx = rx + ru
				pc += 3
			case 2:
				ry = ry + ru
				pc += 3
			case 3:
				rt = rt + ru
				pc += 3
			case 4:
				rp = rp + ru
				pc += 3
			case 5:
				ru = ru + ru
				pc += 3
			}
		}
	case 114:
		switch memory[pc+1] {
		case 1:
			switch memory[pc+2] {
			case 1:
				rx = rx - rx
				pc += 3
			case 2:
				ry = ry - rx
				pc += 3
			case 3:
				rt = rt - rx
				pc += 3
			case 4:
				rp = rp - rx
				pc += 3
			case 5:
				ru = ru - rx
				pc += 3
			}
		case 2:
			switch memory[pc+2] {
			case 1:
				rx = rx - ry
				pc += 3
			case 2:
				ry = ry - ry
				pc += 3
			case 3:
				rt = rt - ry
				pc += 3
			case 4:
				rp = rp - ry
				pc += 3
			case 5:
				ru = ru - ry
				pc += 3
			}
		case 3:
			switch memory[pc+2] {
			case 1:
				rx = rx - rt
				pc += 3
			case 2:
				ry = ry - rt
				pc += 3
			case 3:
				rt = rt - rt
				pc += 3
			case 4:
				rp = rp - rt
				pc += 3
			case 5:
				ru = ru - rt
				pc += 3
			}
		case 4:
			switch memory[pc+2] {
			case 1:
				rx = rx - rp
				pc += 3
			case 2:
				ry = ry - rp
				pc += 3
			case 3:
				rt = rt - rp
				pc += 3
			case 4:
				rp = rp - rp
				pc += 3
			case 5:
				ru = ru - rp
				pc += 3
			}
		case 5:
			switch memory[pc+2] {
			case 1:
				rx = rx - ru
				pc += 3
			case 2:
				ry = ry - ru
				pc += 3
			case 3:
				rt = rt - ru
				pc += 3
			case 4:
				rp = rp - ru
				pc += 3
			case 5:
				ru = ru - ru
				pc += 3
			}
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
			pc += 2
		case 2:
			stack[sp] = ry
			sp += 1
			pc += 2
		case 3:
			stack[sp] = rt
			sp += 1
			pc += 2
		case 4:
			stack[sp] = rp
			pc += 2
		case 5:
			stack[sp] = ru
			pc += 2
		}
	case 118:
		switch memory[pc+1] {
		case 1:
			rx = stack[sp]
			pc += 2
		case 2:
			ry = stack[sp]
			pc += 2
		case 3:
			rt = stack[sp]
			pc += 2
		case 4:
			rp = stack[sp]
			pc += 2
		case 5:
			ru = stack[sp]
			pc += 2
		}
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
			pc += 2
		case 2:
			fmt.Print(string(ry))
			pc += 2
		case 3:
			fmt.Print(string(rt))
			pc += 2
		case 4:
			fmt.Print(string(rp))
			pc += 2
		case 5:
			fmt.Print(string(ru))
			pc += 2
		}
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
			pc += 2
		case 2:
			fmt.Print(ry)
			pc += 2
		case 3:
			fmt.Print(rt)
			pc += 2
		case 4:
			fmt.Print(rp)
			pc += 2
		case 5:
			fmt.Print(ru)
			pc += 2
		}
	case 132:
		fmt.Print("\033[H\033[2J")
		pc += 1
	case 150:
		pc += 2
	}
}

func getInstruction() {
	ir = uint8(memory[pc])
}

func debugCheck() {
	if debugDisplay == 1 {
		fmt.Print("\033[H\033[2J")
		fmt.Println("RX:", rx, "RY:", ry, "RT:", rt, "RP:", rp, "RU:", ru)
		fmt.Println("PC:", pc, "IR:", ir, "EF:", ef, "MF:", mf, "KB:", memory[65000])
	}
}

func loadRom() {
	fmt.Println("SPE_ - Simple Processor Emulator Plus | Rom Loader")
	var count int = 0 //Memory Counter, place line at this memory address

	//Thanks to stackoverflow and some other golang education website, Still don't understand this
	f, err := os.Open("rom.txt")
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
			fmt.Println("loadAddress Found: Given address", linec, "now count is:", count)

		} else {
			line2, _ := strconv.Atoi(line)
			memory[count] = uint16(line2)
			fmt.Println("line written: Given line *", line2, "* now memory[count] is *", memory[count], "*, count is now", count+1)
			count += 1
		}
	}
	fmt.Println("Finished, 1 seconds until start...")
	time.Sleep(1 * time.Second)
	fmt.Print("\033[H\033[2J")
	f.Close()
}
