.cpu cortex-m0
.text
.align 2
.global or

or:
	PUSH 	{ R4, R5, R6, LR }
	SUB 	R2, R0, R0
	SUB 	R3, R2, #1
	SBC 	R2, R2, R3
	SUB 	R4, R1, R1
	NEG 	R3, R4
	ADC 	R3, R3, R4
	ASR 	R5, R2, #31
	SUB 	R4, R5, R2
	ASR 	R5, R3, #31
	SUB 	R6, R5, R3
	ORR 	R4, R4, R6
	LSR 	R4, R4, #31
END:
	MOVS	R0, R4
	POP 	{ R4, R5, R6, PC }