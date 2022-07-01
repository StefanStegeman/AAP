.cpu cortex-m0
.text
.align 2
.global sommig

sommig:
	PUSH 	{ R4, LR }
	MOVS	R1, #0
LOOP:
	MOVS	R2, #1
	ASR 	R3, R0, #31
	LSR 	R4, R2, #31
	CMP 	R0, R2
	ADC 	R3, R3, R4
	ADD 	R1, R0
	MOVS	R4, #1
	SUB 	R0, R4
	CMP 	R3, #1
	BEQ 	LOOP
END:
	MOVS	R0, R1
	POP 	{ R4, PC }