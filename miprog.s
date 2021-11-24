
.global main
.func main

OutputInt:
    PUSH {LR}          @ store LR since printf call overwrites 
    LDR R0,=result_str  @ string at label hello_str: 
    BL printf           @ call printf, where R1 is the print argument 
    POP {PC}

IF_TRUE1:
	MOV R0, #1 
	POP {PC} 
 
 fact:
	PUSH {LR}
	MOV R4, R1
	cmp R4, #1
	blt IF_TRUE1
	SUB R5, R4, #1 
	MOV R1,R5
	BL fact
	MOV R6, R0
	MOV R6, R7
	MUL R8, R4, R6 
	MOV R0, R8 
	POP {PC} 
 
 main:
	MOV R8, #3
	MOV R1,R8
	BL fact
	MOV R9, R0
	MOV R9, R10
	MOV R1,R9
	BL OutputInt

exit:
	MOV R7, #4          @ write syscall, 4
	MOV R0, #1          @ output stream to monitor, 1
	MOV R2, #21         @ print string length
	LDR R1,=exit_str    @ string at label exit_str:
	SWI 0               @ execute syscall


    MOV R7, #1          @ terminate syscall, 1
	SWI 0               @ execute syscall
.data 
add_str: 
.ascii "Adding numbers... \n"
result_str: 
.asciz "Sum = %d\n"
 exit_str: 
.ascii "Terminating program."  