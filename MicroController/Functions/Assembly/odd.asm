.cpu cortex-m0
.text
.align 2
.global odd

odd:
	PUSH 	{ LR }
	MOVS	R1, #0
	SUB 	R3, R1, R0
	NEG 	R2, R3
	ADC 	R2, R2, R3
	CMP 	R2, #1
	BNE 	.L2
	MOVS	R3, #0
	B   	.L4
.L2:
	MOVS	R1, #1
	SUB 	R0, R1
	BL  	even
.L4:
END:
	MOVS	R0, R3
	POP 	{ PC }