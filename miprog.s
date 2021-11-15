
.global main
.func main

OutputInt:

	MOV R4, LR          @ store LR since printf call overwrites
	LDR R0,=result_str  @ string at label hello_str:
	BL printf           @ call printf, where R1 is the print argument
	MOV LR, R4          @ restore LR from R4
	MOV PC, LR          @ return

main:
	MOV R0, #9
 	ADD R1, R0, #3 
	MOV R2, R1
	MOV R1,R2
	MOV R2,R0
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