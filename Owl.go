//Owl.go
/*
___________________
Owl Virtual Machine

v1.2.0

1/2/23
___________________
MIT License

Copyright (c) 2022-2023 thepiger4009

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
______________________________________________________________________________
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

type owl_core struct { //

	//_________
	//Registers
	//____________________________________________________________
	x, y, t, p, u uint32 //32bit Index Registers
	o             uint8  //8bit Opcode Register
	r             uint32 //32bit Software Interrupt Watch Register
	//____________________________________________________________

	//________
	//Pointers
	//_______________________________
	ijp uint32 //Interrupt Jump Point
	pc  uint32 //Program Counter
	sp  uint8  //Stack Pointer
	//_______________________________

	//_____
	//Flags
	//_______________________________________________
	e, m, i byte //Byte Flags: equal, math, interrupt
	//_______________________________________________

	//_____
	//Stack
	//_____________________________
	stack [256]uint32 //32bit Stack
	//_____________________________

}

// Declare Instances
// _______________________________________________
var cpu1 owl_core      //Central Processing Unit1
var mem [524288]uint32 //Memory Addresses

var display_statistics byte = 0 //Display Processor Statistics
//_______________________________________________

// Owl Virtual Machine Functions
// __________
func main() {
	owlInit()
}

func owl_error_report(error_type string) {
	display_statistics = 0
	fmt.Print("\033[H\033[2J")
	fmt.Println("Hello there! It seems something went wrong with your Owl Virtual Machine instance.")
	fmt.Println("I am a error reporter and was triggered by", error_type, ".")
	fmt.Println("")
	fmt.Println("Statistics of this Owl Virtual Machine instance on error:")
	fmt.Println("x:", cpu1.x, "y:", cpu1.y, "t:", cpu1.t, "p:", cpu1.pc, "u:", cpu1.u, "o:", cpu1.o, "r:", cpu1.r, "key:", mem[524287])
	fmt.Println("pc:", cpu1.pc, "sp:", cpu1.sp, "ijp:", cpu1.ijp, "e:", cpu1.e, "m:", cpu1.m, "i:", cpu1.i)
	fmt.Println("")
	fmt.Println("")
	fmt.Println("This report and instance will close in 10 seconds. You can close out of it now if you don't want to wait.")
	time.Sleep(10 * time.Second)
	os.Exit(4)
}

// Owl Virtual Machine Exectuion Functions
// ___________
func owlInit() {

	//___________________________________
	//Load any outside source into memory
	//___________________________________
	loadRom()
	loadProgram()
	//___________________________________

	//_____________
	//Keyboard Main
	//________________________________________
	go func() {
		for {
			key, _, err := keyboard.GetSingleKey()
			if err != nil {
				panic(err)
			}
			mem[524287] = uint32(key)
			switch mem[524287] {
			case 92:
				os.Exit(4)
			case 95:
				switch display_statistics {
				case 1:
					display_statistics = 0
					fmt.Print("\033[H\033[2J")
				case 0:
					display_statistics = 1
				}
			case 0:
				mem[524287] = 32
			}
		}
	}()
	//________________________________________

	//__________
	//Timer Main
	//___________________________
	go func() {
		for {
			mem[524286] += 1
			if mem[524286] > 60 {
				mem[524286] = 0
			}
		}
	}()
	//___________________________

	//_________________
	//Statistic Display
	//_____________________________________________________________________________________________________________________________________________
	go func() {
		for {
			if display_statistics == 1 {
				fmt.Println("x:", cpu1.x, "y:", cpu1.y, "t:", cpu1.t, "p:", cpu1.p, "u:", cpu1.u, "o:", cpu1.o, "r:", cpu1.r, "key:", mem[524287])
				fmt.Println("pc:", cpu1.pc, "sp:", cpu1.sp, "ijp:", cpu1.ijp, "e:", cpu1.e, "m:", cpu1.m, "i:", cpu1.i)
				fmt.Println("______________________________________")
			}
		}
	}()
	//_____________________________________________________________________________________________________________________________________________
	owl_execution_loop()
}

func loadRom() { //This section is a modified segment of some code from a golang learning site, and stackoverflow. Thanks to whoever made it.
	var count int = 0
	f, err := os.Open("rom.bin")
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(f)
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
			mem[count] = uint32(line2)
			count += 1
		}
	}
	f.Close()
}

func loadProgram() {
	var count int = 0
	file := os.Args[1:]
	ffile := strings.Join(file, " ")
	f, err := os.Open(ffile)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "loadAddress" {
			scanner.Scan()
			line := scanner.Text()
			linec, _ := strconv.Atoi(line)
			count = linec
		} else {
			line2, _ := strconv.Atoi(line)
			mem[count] = uint32(line2)
			count += 1
		}
	}
	fmt.Println("Owl | Init.")
	time.Sleep(1 * time.Second)
	fmt.Print("\033[H\033[2J")
	f.Close()
}

func owl_execution_loop() {
	for {
		cpu1_cycle()
	}
}

// Owl Virtual Machine CPU1 functions
// _____
func cpu1_cycle() {
	cpu1_fetch()
	cpu1_decode()
}

func cpu1_fetch() {
	cpu1.o = uint8(mem[cpu1.pc])
}

func cpu1_decode() {
	if cpu1.o < 100 {
		owl_error_report("[OPCODE ERROR: Unknown Opcode]")
	}
	switch cpu1.o {
	case 0:
		owl_error_report("[OPCODE REPORTED AS 0/NO OPCODE GIVEN]")
	case 100:
		mov_dec() //mov #1,x
	case 101:
		mov_address() //mov $0400,x
	case 102:
		mov_addressP() //mov p%400,x
	case 103:
		mov_addressU() //mov u%400,x
	case 104:
		mov_intoAddress() //mov x,$400
	case 105:
		mov_intoAddressP() //mov x,p%400
	case 106:
		mov_intoAddressU() //mov x,u%400
	case 107:
		increase() //inc x
	case 108:
		decrease() //dec x
	case 109:
		mov_regIntoReg() //mov x,y
	case 110:
		jump() //jmp $400
	case 111:
		beq() //beq $400
	case 112:
		bne() //bne $400
	case 113:
		add() //add x,y
	case 114:
		sub() //sub y,x
	case 115:
		cmp_dec() //cmp x,#5
	case 116:
		set_e() //sef 0
	case 117:
		mov_ontoStack() //mov x,stack
	case 118:
		mov_stackOntoReg() //mov stack,x
	case 119:
		increase_stackPointer() //isp
	case 120:
		decrease_stackPointer() //dsp
	case 121:
		no_operation() //nop
	case 122:
		display_regAscii() //dra x
	case 123:
		display_backspace() //dbk
	case 124:
		jsr() //jsr $400
	case 125:
		rts() //rts
	case 126:
		mov_pcOntoStack() //mov pc,stack
	case 127:
		cmp_regWreg() //cmp x,y
	case 128:
		display_enter() //den
	case 129:
		display_regValue() //drv x
	case 130:
		display_clear() //dcs
	case 131:
		display_space() //dsn
	}
}

//Instructions
//______________

// _____________________________
func mov_dec() { //mov #1,x
	switch mem[cpu1.pc+1] {
	case 1:
		cpu1.x = mem[cpu1.pc+2]
	case 2:
		cpu1.y = mem[cpu1.pc+2]
	case 3:
		cpu1.t = mem[cpu1.pc+2]
	case 4:
		cpu1.p = mem[cpu1.pc+2]
	case 5:
		cpu1.u = mem[cpu1.pc+2]
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func mov_address() { //mov $400,x
	switch mem[cpu1.pc+1] {
	case 1:
		cpu1.x = mem[mem[cpu1.pc+2]]
	case 2:
		cpu1.y = mem[mem[cpu1.pc+2]]
	case 3:
		cpu1.t = mem[mem[cpu1.pc+2]]
	case 4:
		cpu1.p = mem[mem[cpu1.pc+2]]
	case 5:
		cpu1.u = mem[mem[cpu1.pc+2]]
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func mov_addressP() { //mov p%400,x
	switch mem[cpu1.pc+1] {
	case 1:
		cpu1.x = mem[mem[cpu1.pc+2]+cpu1.p]
	case 2:
		cpu1.y = mem[mem[cpu1.pc+2]+cpu1.p]
	case 3:
		cpu1.t = mem[mem[cpu1.pc+2]+cpu1.p]
	case 4:
		cpu1.p = mem[mem[cpu1.pc+2]+cpu1.p]
	case 5:
		cpu1.u = mem[mem[cpu1.pc+2]+cpu1.p]
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func mov_addressU() { //mov u%400,x
	switch mem[cpu1.pc+1] {
	case 1:
		cpu1.x = mem[mem[cpu1.pc+2]+cpu1.u]
	case 2:
		cpu1.y = mem[mem[cpu1.pc+2]+cpu1.u]
	case 3:
		cpu1.t = mem[mem[cpu1.pc+2]+cpu1.u]
	case 4:
		cpu1.p = mem[mem[cpu1.pc+2]+cpu1.u]
	case 5:
		cpu1.u = mem[mem[cpu1.pc+2]+cpu1.u]
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func mov_intoAddress() { //mov x,$400
	switch mem[cpu1.pc+1] {
	case 1:
		mem[mem[cpu1.pc+2]] = cpu1.x
	case 2:
		mem[mem[cpu1.pc+2]] = cpu1.y
	case 3:
		mem[mem[cpu1.pc+2]] = cpu1.t
	case 4:
		mem[mem[cpu1.pc+2]] = cpu1.p
	case 5:
		mem[mem[cpu1.pc+2]] = cpu1.u
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func mov_intoAddressP() { //mov x,p%400
	switch mem[cpu1.pc+1] {
	case 1:
		mem[mem[cpu1.pc+2]+cpu1.p] = cpu1.x
	case 2:
		mem[mem[cpu1.pc+2]+cpu1.p] = cpu1.y
	case 3:
		mem[mem[cpu1.pc+2]+cpu1.p] = cpu1.t
	case 4:
		mem[mem[cpu1.pc+2]+cpu1.p] = cpu1.p
	case 5:
		mem[mem[cpu1.pc+2]+cpu1.p] = cpu1.u
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func mov_intoAddressU() { //mov x,u%400
	switch mem[cpu1.pc+1] {
	case 1:
		mem[mem[cpu1.pc+2]+cpu1.u] = cpu1.x
	case 2:
		mem[mem[cpu1.pc+2]+cpu1.u] = cpu1.y
	case 3:
		mem[mem[cpu1.pc+2]+cpu1.u] = cpu1.t
	case 4:
		mem[mem[cpu1.pc+2]+cpu1.u] = cpu1.p
	case 5:
		mem[mem[cpu1.pc+2]+cpu1.u] = cpu1.u
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func increase() { //inc x
	switch mem[cpu1.pc+1] {
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
}

//_____________________________

//_____________________________

func decrease() { //dec x
	switch mem[cpu1.pc+1] {
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
}

//_____________________________

// _____________________________
func mov_regIntoReg() { //mov x,y
	switch mem[cpu1.pc+1] {
	case 1:
		switch mem[cpu1.pc+2] {
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
	case 2:
		switch mem[cpu1.pc+2] {
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
	case 3:
		switch mem[cpu1.pc+2] {
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
	case 4:
		switch mem[cpu1.pc+2] {
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
	case 5:
		switch mem[cpu1.pc+2] {
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
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func jump() { //jmp $400
	cpu1.pc = mem[cpu1.pc+1]
}

//_____________________________

// _____________________________
func beq() { //beq $400
	if cpu1.e == 1 {
		cpu1.pc = mem[cpu1.pc+1]
		cpu1.e = 0
	} else {
		cpu1.pc += 2
	}
}

//_____________________________

// _____________________________
func bne() { //bne $400
	if cpu1.e == 0 {
		cpu1.pc = mem[cpu1.pc+1]
	} else {
		cpu1.pc += 2
	}
}

//_____________________________

// _____________________________
func add() { //add x,y
	switch mem[cpu1.pc+1] {
	case 1:
		switch mem[cpu1.pc+2] {
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
	case 2:
		switch mem[cpu1.pc+2] {
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
	case 3:
		switch mem[cpu1.pc+2] {
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
	case 4:
		switch mem[cpu1.pc+2] {
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
	case 5:
		switch mem[cpu1.pc+2] {
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
	}
	cpu1.m = 1
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func sub() { //sub x,y
	switch mem[cpu1.pc+1] {
	case 1:
		switch mem[cpu1.pc+2] {
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
	case 2:
		switch mem[cpu1.pc+2] {
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
	case 3:
		switch mem[cpu1.pc+2] {
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
	case 4:
		switch mem[cpu1.pc+2] {
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
	case 5:
		switch mem[cpu1.pc+2] {
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
	}
	cpu1.m = 1
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func cmp_dec() { //cmp x,#5
	switch mem[cpu1.pc+1] {
	case 1:
		if cpu1.x == mem[cpu1.pc+2] {
			cpu1.e = 1
		}
	case 2:
		if cpu1.y == mem[cpu1.pc+2] {
			cpu1.e = 1
		}
	case 3:
		if cpu1.t == mem[cpu1.pc+2] {
			cpu1.e = 1
		}
	case 4:
		if cpu1.p == mem[cpu1.pc+2] {
			cpu1.e = 1
		}
	case 5:
		if cpu1.u == mem[cpu1.pc+2] {
			cpu1.e = 1
		}
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func set_e() { //sef 0
	switch mem[cpu1.pc+1] {
	case 1:
		cpu1.e = 1
	case 0:
		cpu1.e = 0
	}
	cpu1.pc += 2
}

//_____________________________

// _____________________________
func mov_ontoStack() { //mov x,stack
	switch mem[cpu1.pc+1] {
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
		cpu1.sp += 1
	case 5:
		cpu1.stack[cpu1.sp] = cpu1.u
		cpu1.sp += 1
	}
	cpu1.pc += 2
}

//_____________________________

// _____________________________
func mov_stackOntoReg() { //mov stack,x
	switch mem[cpu1.pc+1] {
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
}

//_____________________________

// _____________________________
func increase_stackPointer() { //isp
	cpu1.sp += 1
	cpu1.pc += 1
}

//_____________________________

// _____________________________
func decrease_stackPointer() { //dsp
	cpu1.sp -= 1
	cpu1.pc += 1
}

//_____________________________

// _____________________________
func no_operation() { //nop
	cpu1.pc += 1
}

//_____________________________

// _____________________________
func display_regAscii() { //dra x
	switch mem[cpu1.pc+1] {
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
}

//_____________________________

// _____________________________
func display_backspace() { //dbk
	fmt.Printf("\b \b")
	cpu1.pc += 1
}

//_____________________________

// _____________________________
func jsr() { //jsr $400
	cpu1.stack[cpu1.sp] = cpu1.pc + 2
	cpu1.sp += 1
	cpu1.pc = mem[cpu1.pc+1]
}

//_____________________________

// _____________________________
func rts() { //rts
	cpu1.sp -= 1
	cpu1.pc = cpu1.stack[cpu1.sp]
}

//_____________________________

// _____________________________
func mov_pcOntoStack() { //mov pc,stack
	cpu1.stack[cpu1.sp] = cpu1.pc
	cpu1.sp += 1
	cpu1.pc += 1
}

//_____________________________

// _____________________________
func cmp_regWreg() { //cmp x,y
	switch mem[cpu1.pc+1] {
	case 1:
		switch mem[cpu1.pc+2] {
		case 1:
			if cpu1.x == cpu1.x {
				cpu1.e = 1
			}
		case 2:
			if cpu1.x == cpu1.y {
				cpu1.e = 1
			}
		case 3:
			if cpu1.x == cpu1.t {
				cpu1.e = 1
			}
		case 4:
			if cpu1.x == cpu1.p {
				cpu1.e = 1
			}
		case 5:
			if cpu1.x == cpu1.u {
				cpu1.e = 1
			}
		}
	case 2:
		switch mem[cpu1.pc+2] {
		case 1:
			if cpu1.y == cpu1.x {
				cpu1.e = 1
			}
		case 2:
			if cpu1.y == cpu1.y {
				cpu1.e = 1
			}
		case 3:
			if cpu1.y == cpu1.t {
				cpu1.e = 1
			}
		case 4:
			if cpu1.y == cpu1.p {
				cpu1.e = 1
			}
		case 5:
			if cpu1.y == cpu1.u {
				cpu1.e = 1
			}
		}
	case 3:
		switch mem[cpu1.pc+2] {
		case 1:
			if cpu1.t == cpu1.x {
				cpu1.e = 1
			}
		case 2:
			if cpu1.t == cpu1.y {
				cpu1.e = 1
			}
		case 3:
			if cpu1.t == cpu1.t {
				cpu1.e = 1
			}
		case 4:
			if cpu1.t == cpu1.p {
				cpu1.e = 1
			}
		case 5:
			if cpu1.t == cpu1.u {
				cpu1.e = 1
			}
		}
	case 4:
		switch mem[cpu1.pc+2] {
		case 1:
			if cpu1.p == cpu1.x {
				cpu1.e = 1
			}
		case 2:
			if cpu1.p == cpu1.y {
				cpu1.e = 1
			}
		case 3:
			if cpu1.p == cpu1.t {
				cpu1.e = 1
			}
		case 4:
			if cpu1.p == cpu1.p {
				cpu1.e = 1
			}
		case 5:
			if cpu1.p == cpu1.u {
				cpu1.e = 1
			}
		}
	case 5:
		switch mem[cpu1.pc+2] {
		case 1:
			if cpu1.u == cpu1.x {
				cpu1.e = 1
			}
		case 2:
			if cpu1.u == cpu1.y {
				cpu1.e = 1
			}
		case 3:
			if cpu1.u == cpu1.t {
				cpu1.e = 1
			}
		case 4:
			if cpu1.u == cpu1.p {
				cpu1.e = 1
			}
		case 5:
			if cpu1.u == cpu1.u {
				cpu1.e = 1
			}
		}
	}
	cpu1.pc += 3
}

//_____________________________

// _____________________________
func display_enter() { //den
	fmt.Println("")
	cpu1.pc += 1
}

//_____________________________

// _____________________________
func display_regValue() { //drv
	switch mem[cpu1.pc+1] {
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
}

//_____________________________

// _____________________________
func display_clear() { //dcs
	fmt.Print("\033[H\033[2J")
	cpu1.pc += 1
}

//_____________________________

// _____________________________
func display_space() { //dsn
	fmt.Print(" ")
	cpu1.pc += 1
}

//_____________________________
