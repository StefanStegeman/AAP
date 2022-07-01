.cpu cortex-m0
.text
.align 2
.global andTest

andTest:
	PUSH 	{ R4, R5, R6, LR }
	SUB 	R3, R0, R0
	NEG 	R2, R3
	ADC 	R2, R2, R3
	SUB 	R4, R1, R1
	NEG 	R3, R4
	ADC 	R3, R3, R4
	ASR 	R5, R2, #31
	SUB 	R4, R5, R2
	ASR 	R5, R3, #31
	SUB 	R6, R5, R3
	AND 	R4, R4, R6
	LSR 	R4, R4, #31
END:
	MOVS	R0, R4
	POP 	{ R4, R5, R6, PC }