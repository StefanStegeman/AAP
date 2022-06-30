.cpu cortex-m0
.text
.align 2
.global AndTest

AndTest:
	PUSH 	{ R4, R5, R6, R7, LR }
	MOVS	R1, #1
	SUB 	R3, R1, R0
	NEG 	R2, R3
	ADC 	R2, R2, R3
	MOVS	R3, #2
	SUB 	R4, R3, R0
	SUB 	R5, R4, #1
	SBC 	R4, R4, R5
	ASR 	R6, R2, #31
	SUB 	R5, R6, R2
	ASR 	R6, R4, #31
	SUB 	R7, R6, R4
	AND 	R5, R5, R7
	LSR 	R5, R5, #31
END:
	MOVS	R0, R5
	POP 	{ R4, R5, R6, R7, PC }