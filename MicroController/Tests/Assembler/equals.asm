.cpu cortex-m0
.text
.align 2
.global equals

equals:
	PUSH 	{ LR }
	SUB 	R3, R1, R0
	NEG 	R2, R3
	ADC 	R2, R2, R3
END:
	MOVS	R0, R2
	POP 	{ PC }