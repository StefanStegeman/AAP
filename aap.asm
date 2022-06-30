.cpu cortex-m0
.text
.align 2
.global equals

equals:
	PUSH 	{ LR }
	MOVS	R1, #1
	POP 	{ PC }