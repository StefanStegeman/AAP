.cpu cortex-m0
.text
.align 2
.global less

less:
	PUSH 	{ LR }
	MOV 	R2, #1
	CMP 	R0, R1
	BLT 	.L2
	MOVS	R2, #0
.L2:
END:
	MOVS	R0, R2
	POP 	{ PC }