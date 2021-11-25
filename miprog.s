
.global main
.func main

OutputInt:
    PUSH {LR}          @ store LR since printf call overwrites 
    LDR R0,=result_str  @ string at label hello_str: 
    BL printf           @ call printf, where R1 is the print argument 
    POP {PC}

IF_TRUE1:
 	ADD R6, R2, #1 
	MOV R0, R6 
	POP {PC} 
 
 IF_TRUE2:
	SUB R7, R1, #1 
	MOV R1,R7
	MOV R2, #1
	BL ackerman
	MOV R8, R0
	MOV R0, R8 
	POP {PC} 
 
 IF_FALSE2:
	SUB R9, R2, #1 
	MOV R1,R4
	MOV R2,R9
	BL ackerman
	MOV R10, R0
	MOV R11, R10
	SUB R12, R1, #1 
	MOV R1,R12
	MOV R2,R11
	BL ackerman
	MOV R5, R0
	MOV R0, R5
	POP {PC} 
 
 ackerman:
	PUSH {LR}
	MOV R4, R1
	MOV R5, R2
	MOV R1,R5
	BL OutputInt
	cmp R4, #0
	beq IF_TRUE1
	cmp R5, #0
	beq IF_TRUE2
	B IF_FALSE2
main:
	MOV R1,#0
	MOV R2,#1
	BL ackerman
	MOV R1, R0
	bl OutputInt

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
