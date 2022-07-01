.cpu cortex-m0
.text
.align 2
.global factorial

factorial:
	PUSH 	{ R4, LR }
	MOVS	R1, #1
LOOP:
	MOVS	R2, #0
	MOV 	R3, #1
	CMP 	R0, R2
	BGT 	.L2
	MOVS	R3, #0
	MUL 	R1, R0
	MOVS	R4, #1
	SUB 	R0, R4
	CMP 	R3, #1
	BEQ 	LOOP
END:
	MOVS	R0, R1
	POP 	{ R4, PC }