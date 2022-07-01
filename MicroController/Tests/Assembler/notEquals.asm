.cpu cortex-m0
.text
.align 2
.global notEquals

notEquals:
	PUSH 	{ LR }
	SUB 	R2, R1, R0
	SUB 	R3, R2, #1
	SBC 	R2, R2, R3
END:
	MOVS	R0, R2
	POP 	{ PC }