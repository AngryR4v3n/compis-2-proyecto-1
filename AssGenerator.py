
class AssGenerator():
    def __init__(self):
        self.head = ''
        self.main = ''
        self.body = ''
        self.tail = ''
        self.f = open('miprog.s', 'w')
        self.registers_av = {"R1": "","R2": "PARAM", "R3": "PARAM", "R4": "PARAM", "R5": "", "R6": "", "R7": "", "R8": "" , "R9": "" , "R10": "", "R11": "", "R12": ""}
        self.param_registers = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7']
        self.cmpOps = {"<": 'bgt'}
        self.flagBranch = None
        self.intermediate = open('.code.txt', 'r').readlines()
        self.createHead()
        self.createExit()
        self.createTail()
        self.function_identifier(self.intermediate)
        self.write()


    def createHead(self):
        self.head += """
.global main
.func main\n
"""

    def createTail(self):
        self.tail += ".data \n"
        self.tail += "add_str: \n"
        self.tail += r'.ascii "Adding numbers... \n"'
        self.tail += "\nresult_str: \n"
        self.tail += r'.asciz "Sum = %d\n"'
        self.tail += "\n exit_str: \n"
        self.tail += '.ascii "Terminating program."  '


    # Obtenido de https://raw.githubusercontent.com/cmcmurrough/cse2312/
    def createExit(self):

        #Procedimiento de exit
        self.exit = """
exit:
	MOV R7, #4          @ write syscall, 4
	MOV R0, #1          @ output stream to monitor, 1
	MOV R2, #21         @ print string length
	LDR R1,=exit_str    @ string at label exit_str:
	SWI 0               @ execute syscall


    MOV R7, #1          @ terminate syscall, 1
	SWI 0               @ execute syscall\n"""

    def createPrint(self):
        #procedimiento
        self.body += """
	MOV R4, LR          @ store LR since printf call overwrites
	LDR R0,=result_str  @ string at label hello_str:
	BL printf           @ call printf, where R1 is the print argument
	MOV LR, R4          @ restore LR from R4
	MOV PC, LR          @ return\n
"""

    def function_identifier(self,content):
        paramCounter = 1
        for number, line in enumerate(content):
            
            if line.find('function') > -1:
                name = line.split('function')[1].strip()
                self.body += f'{name}\n'
                #restart de param counter si entramos a nueva funcion
                paramCounter = 1

                if name.find('OutputInt') > -1 :
                    self.createPrint()
                
                    

            #convertir instrucciones
            splitted = line.strip().split(' ')
            for i, elem in enumerate(splitted):
                elem = elem.strip()

                if '=' in splitted and len(splitted) > 3:
                    if elem == '+':
                        self.body += f" \tADD {self.getReg(splitted[0])}, {self.getReg(splitted[i-1])}, {self.getReg(splitted[i+1].strip())} \n"
                        continue
                    elif elem == '-':
                        self.body += f"\tSUB {self.getReg(splitted[0])}, {self.getReg(splitted[i-1])}, {self.getReg(splitted[i+1].strip())} \n"
                        continue
                    elif elem == '*':
                        self.body += f"\tMUL {self.getReg(splitted[0])}, {self.getReg(splitted[i-1])}, {self.getReg(splitted[i+1].strip())} \n"
                        continue

                elif elem == '=' and not len(splitted) > 3:
                    
                    self.body += f"\tMOV {self.getReg(splitted[i-1])}, {self.getReg(splitted[-1].strip())}\n"

                    if splitted[-1].find('t') > -1:
                        self.freeReg(splitted[-1].strip())

                    continue


                if elem == 'RETURN':
                    variableToReturn = splitted[i + 1]
                    self.body += f'\tMOV R0, {variableToReturn} \n'
                    self.body += f'\tret \n'

                if elem == 'PARAM':
                    innerCounter = 1
                    if content[number + 1].find('OutputInt') > -1:
                        self.body += self.getRegParam(splitted[i+1], 1)
                    else:
                        self.body += self.getRegParam(splitted[i+1],innerCounter)

                if elem == 'CALL':
                    functionName = splitted[i+1].replace(',','')

                    if functionName.find('OutputInt') > -1:

                        self.body += '\tBL OutputInt\n'

                    else:
                        self.body += f'\tBL {functionName}\n'

                if elem.find("WHILE") > -1:
                    if elem[-1] == ':':
                        self.body += f'{elem}\n'

                if elem.find("END_WHILE") > -1:
                    if elem[-1] == ':':
                        self.body += f'{elem}\n'

                if elem.find("PARAMETER") > -1 and name != 'OutputInt:':
                    register = f'R{paramCounter}'
                    self.registers_av[register] = 'PARAM'

                    regi = self.getReg(splitted[i+1].strip())

                    self.body += f'MOV {regi}, {register}\n'
                    paramCounter += 1

                #Para operaciones condicionales.
                if elem in self.cmpOps.keys():
                    self.flagBranch = self.cmpOps[elem]
                    reg = self.getReg(splitted[i-1])
                    reg2 = self.getReg(splitted[i+1])
                    self.body += f'cmp {reg}, {reg2}\n'


                if elem.find('IFZ') > -1:
                    if self.flagBranch != None:    
                        self.body += f'{self.flagBranch} {splitted[-1].strip()}\n'
                        
                
                if elem.find('GOTO') > -1:
                    
                    if splitted[0].strip() == 'GOTO':
                        self.body += f'\tb {splitted[1]}\n'


    def write(self):
        #headers
        self.f.write(self.head)
        print(self.head)
        #main
        self.f.write(self.main)
        print(self.main)
        #body
        self.f.write(self.body)
        print(self.body)

        #createExit
        self.f.write(self.exit)

        self.f.write(self.tail)

        print('============')
        print(self.registers_av)

        self.f.close()


    def getReg(self, var):
        register = None
        #en el caso que ya este guardado antes return el registro en donde esta
        var = var.strip()

        if var.find("[") > -1 or var.find("t") > -1:
            for i in self.registers_av.keys():
                if self.registers_av[i] == var:
                    register = i
                    break

            if register != None:
                return register
            else:
                #en el caso que no este guardado busco uno vacio y le asigno a ese registro vacio el valor de var
                for i in self.registers_av.keys():
                    if self.registers_av[i] == "":
                        self.registers_av[i] = var
                        register = i
                        break

                if register != None:
                    return register
                else:
                    return "OUT OF REGISTERS PAPAITO\n finito compadre."
        else:
            return "#"+var



    def getRegParam(self, var, counter):
        register = None
        var = var.strip()
        for i in self.registers_av.keys():
            if self.registers_av[i] == var:
                register = i
                break

        new_reg = "R" + str(counter)
        content = self.registers_av[new_reg]
        if content != "" and content != 'PARAM' and register != new_reg:
            regi3 = None
            for i in self.registers_av.keys():
                if self.registers_av[i] == "":
                    self.registers_av[i] = var
                    regi3 = i
                    break

            #muevo el valor del parametro a un registro cualquiera
            arm_code = "\tMOV " + regi3 + "," + register + "\n"
            arm_code  += "\tMOV " + register + "," + new_reg + "\n"
            arm_code  += "\tMOV " + new_reg + "," + regi3 + "\n"


            #intercambio de variables en descriptor
            self.registers_av[register] = content
            self.registers_av[new_reg] = self.registers_av[regi3]
            self.registers_av[regi3] = ""

            #print("entre primer if ")
            return arm_code
        
        elif register != new_reg:
            arm_code = "\tMOV " + new_reg + "," + register + "\n"
            
            return arm_code
        else:
            return ""


    def freeReg(self, var):
        for i in self.registers_av.keys():
            if self.registers_av[i] == var:
                self.registers_av[i] = ''
                break