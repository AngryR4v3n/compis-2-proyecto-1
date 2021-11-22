
.global main
.func main

OutputInt:
    PUSH {LR}          @ store LR since printf call overwrites 
    LDR R0,=result_str  @ string at label hello_str: 
    BL printf           @ call printf, where R1 is the print argument 
    POP {PC}

WHILE_1:
	cmp R6, R1
	bgt END_WHILE_1
	MOV R6,R2
	MOV R2,R1
	MOV R1,R6
	BL OutputInt
 	ADD R6, R1, R3 
	MOV R4, R6
	MOV R1, R3
	MOV R3, R4
 	ADD R6, R5, #1 
	MOV R5, R6
fib:
	PUSH {LR}
	MOV R1, R0
	MOV R2, #0
	MOV R3, #1
	MOV R4, #0
	MOV R5, #0
	b WHILE_1
END_WHILE_1:
	b exit 
main:
	PUSH {LR}
	MOV R6, #7
	MOV R7,R6
	MOV R6,R1
	MOV R1,R7
	MOV R1, R1 
	BL fib

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