
class AssGenerator():
    def __init__(self):
        self.head = ''
        self.main = ''
        self.body = ''
        self.tail = ''
        self.f = open('miprog.s', 'w')
        self.registers_av = {"R0": "", "R1": "","R2": "", "R3": "", "R4": "", "R5": "", "R6": "", "R7": "", "R8": "" , "R9": "" , "R10": "", "R11": "", "R12": ""}
        self.param_registers = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7']
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
        for number, line in enumerate(content):
            if line.find('function') > -1:
                name = line.split('function')[1].strip()
                self.body += f'{name}\n'

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
                    self.body += f'\tMOV R0, {variableToReturn}'
                    self.body += f'\tret \n'

                if elem == 'PARAM':
                    innerCounter = 0
                    if content[number + 1].find('OutputInt') > -1:
                        self.body += self.getRegParam(splitted[i+1], 1)
                    else:
                        self.body += self.getRegParam(splitted[i+1],innerCounter)

                if elem == 'CALL':
                    functionName = splitted[i+1].replace(',','')

                    if functionName.find('OutputInt') > -1:
                        self.body += self.freeR0()

                        self.body += '\tBL OutputInt\n'

                    else:
                        self.body += f'\tBL {functionName}\n'

                #if elem.find("WHILE") > -1:
                 #   self.body += f'loop_{}:'




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
                    return "OUT OF REGISTERS PAPAITO"
        else:
            return "#"+var


    def freeR0(self):
        code = ''
        if self.registers_av['R0'] == '':
            pass
        else:
            regis = None
            content = self.registers_av['R0']
            for i in self.registers_av.keys():
                if self.registers_av[i] == '':
                    regis = i
                    break

            code = "\tMOV " + regis + "," + "R0" + "\n"
            self.registers_av['R0'] = ''
            self.registers_av[regis] = content


        return code



    def getRegParam(self, var, counter):
        register = None
        var = var.strip()
        for i in self.registers_av.keys():
            if self.registers_av[i] == var:
                register = i
                break

        new_reg = "R" + str(counter)
        content = self.registers_av[new_reg]
        if content != "" and register != new_reg:
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
            self.registers_av[new_reg] = self.registers_av[register]
            self.registers_av[register] = ''
            #print("entre en el else")
            return arm_code
        else:
            return ""


    def freeReg(self, var):
        for i in self.registers_av.keys():
            if self.registers_av[i] == var:
                self.registers_av[i] = ''
                break