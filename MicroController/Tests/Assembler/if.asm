.cpu cortex-m0
.text
.align 2
.global if

if:
	PUSH 	{ LR }
	SUB 	R2, R0, R0
	NEG 	R1, R2
	ADC 	R1, R1, R2
	CMP 	R1, #1
	BNE 	.L2
	MOVS	R2, #1
	B   	.L4
.L2:
.L4:
END:
	MOVS	R0, R2
	POP 	{ PC }