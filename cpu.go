package main

type core struct {
	stack [256]uint16

	rx, ry, rt, rp, ru uint16
	ir, sp             uint8
	pc                 uint16
	ef, mf             uint8
	hei                uint8
}

func setup() {

}
