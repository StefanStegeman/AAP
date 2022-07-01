.cpu cortex-m0
.text
.align 2
.global else

else:
	PUSH 	{ LR }
	SUB 	R1, R0, R0
	SUB 	R2, R1, #1
	SBC 	R1, R1, R2
	CMP 	R1, #1
	BNE 	.L2
	MOVS	R2, #1
	B   	.L4
.L2:
	MOVS	R1, #2
.L4:
END:
	MOVS	R0, R2
	POP 	{ PC }