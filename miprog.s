
.global main
.func main

OutputInt:

	MOV R4, LR          @ store LR since printf call overwrites
	LDR R0,=result_str  @ string at label hello_str:
	BL printf           @ call printf, where R1 is the print argument
	MOV LR, R4          @ restore LR from R4
	MOV PC, LR          @ return

fib:
MOV R5, R1
	MOV R6, #0
	MOV R7, #1
	MOV R8, #0
	MOV R9, #0
WHILE_1:
cmp R9, R5
bgt END_WHILE_1
	MOV R1,R6
	BL OutputInt
 	ADD R10, R6, R7 
	MOV R8, R10
	MOV R6, R7
	MOV R7, R8
 	ADD R10, R9, #1 
	MOV R9, R10
	b WHILE_1
END_WHILE_1:
    b exit

main:
	MOV R10, #7
	MOV R1,R10
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