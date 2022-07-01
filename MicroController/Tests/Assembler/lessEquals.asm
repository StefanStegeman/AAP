.cpu cortex-m0
.text
.align 2
.global lessEquals

lessEquals:
	PUSH 	{ LR }
	LSR 	R2, R0, #31
	ASR 	R3, R1, #31
	CMP 	R1, R0
	ADC 	R2, R2, R3
END:
	MOVS	R0, R2
	POP 	{ PC }