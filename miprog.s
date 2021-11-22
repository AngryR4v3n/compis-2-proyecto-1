
.global main
.func main

OutputInt:
    PUSH {LR}          @ store LR since printf call overwrites 
    LDR R0,=result_str  @ string at label hello_str: 
    BL printf           @ call printf, where R1 is the print argument 
    POP {PC}

WHILE_1:
	cmp R9, R4
	bgt END_WHILE_1
	MOV R1,R5
	BL OutputInt
 	ADD R9, R5, R6 
	MOV R7, R9
	MOV R5, R6
	MOV R6, R7
 	ADD R9, R8, #1 
	MOV R8, R9
	b WHILE_1
fib:
	PUSH {LR}
	MOV R4, R1
	MOV R5, #0
	MOV R6, #1
	MOV R7, #0
	MOV R8, #0
	b WHILE_1
END_WHILE_1:
	b exit 
	b WHILE_1
main:
	MOV R9, #7
	MOV R1,R9
	MOV R1, R9 
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