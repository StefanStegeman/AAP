.cpu cortex-m0
.text
.align 2
.global greaterEquals

greaterEquals:
	PUSH 	{ LR }
	ASR 	R2, R0, #31
	LSR 	R3, R1, #31
	CMP 	R0, R1
	ADC 	R2, R2, R3
END:
	MOVS	R0, R2
	POP 	{ PC }