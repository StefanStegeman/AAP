.cpu cortex-m0
.text
.align 2
.global fibbo

fibbo:
	PUSH 	{ LR }
	MOVS	R1, #1
	LSR 	R2, R0, #31
	ASR 	R3, R1, #31
	CMP 	R1, R0
	ADC 	R2, R2, R3
	CMP 	R2, #1
	BNE 	.L2
	B   	.L4
.L2:
	MOVS	R1, #1
	SUB 	R0, R1
	BL  	fibbo
	MOVS	R2, #1
	SUB 	R0, R2
	BL  	fibbo
.L4:
	POP 	{ PC }