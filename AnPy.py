from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from CustomListeners import CustomListener
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import sys
filepath = None
global x
global errors
from subprocess import Popen,PIPE
class GUI:
    
    def __init__(self) -> None:
        self.x = None
        self.window = tk.Tk()
        self.window.title("Fran Decaf compiler")
        self.window.rowconfigure(0, minsize=800, weight=1)
        self.window.columnconfigure(1, minsize=800, weight=1)

        self.txt_edit = tk.Text(self.window)
        
        self.fr_buttons = tk.Frame(self.window, relief=tk.RAISED, bd=2)
        self.separator = tk.Frame(self.window, relief=tk.RAISED, bd=2)
        self.terminalSc = tk.Text(self.window, background="black")
        self.btn_open = tk.Button(self.fr_buttons, text="Open", command=self.open_file)
        self.btn_save = tk.Button(self.fr_buttons, text="Save As...", command=self.save_file)
        self.btn_saveNotAs = tk.Button(self.fr_buttons, text="Save", command=self.save)
        self.btn_run = tk.Button(self.fr_buttons, text="Compile", command=self.main)
        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.btn_saveNotAs.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_run.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.separator.grid(row=1, column=1, sticky="ns")
        self.txt_edit.grid(row=0, column=1, sticky="nsew")
        self.terminalSc.grid(row=2, column=1, sticky="nsew")
        terminal = "franCompiler@decaf % ...waiting for input"
        self.terminalSc.insert(tk.END, terminal)
        
        self.SymbolFile = open('symbols.csv', 'w')
        self.window.mainloop()
    
    def subprocess_cmd(self,dr,cmd1,cmd2):
        p1 = Popen(cmd1.split(),stdout=PIPE,cwd=dr)
        p2 = Popen(cmd2.split(),stdin=p1.stdout,stdout=PIPE,cwd=dr)
        p1.stdout.close()
        return p2.communicate()[0]
    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        self.txt_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.txt_edit.insert(tk.END, text)
        self.window.title(f"Fran Decaf compiler - {filepath}")
        self.x = filepath
        self.SymbolFile = open('symbols.csv', 'w')
    
    def save_file(self):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txt_edit.get(1.0, tk.END)
            output_file.write(text)
        self.window.title(f"Fran Decaf compiler- {filepath}")

    def save(self):
        """Save current"""
        filepath = self.x
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txt_edit.get(1.0, tk.END)
            output_file.write(text)

    def main(self):
        terminal = "franCompiler@decaf % "
        
        input_stream = FileStream(self.x)
        lexer = DecafLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DecafParser(stream)
        tree = parser.program()
        walker = ParseTreeWalker()
        Customlisteners = CustomListener()
        walker.walk(Customlisteners, tree)

        if Customlisteners.errors == []:
            self.terminalSc.delete(1.0, tk.END)
            
            self.terminalSc.insert(tk.END, terminal)
            ok = "Successfully compiled! \n"
            self.terminalSc.insert(tk.END, ok)
            self.terminalSc.insert(tk.END, "[*] No errors found \n")
            self.terminalSc.insert(tk.END, "[*] Generated intermediate code \n")
            self.terminalSc.insert(tk.END, "[X] ARM code (to be implemented) \n")
            self.terminalSc.insert(tk.END, "----------------------------------------------- \n")
            self.terminalSc.insert(tk.END, "Printing symbol table as symbols.csv \n")
            #imprimimos en csv los scopes.
            csvHeader = 'SCOPE, TYPE, NAME, OFFSET, ISARRAY, NUM, SIZE \n'
            self.SymbolFile.write(csvHeader)
            for elem in list(Customlisteners.scopes.keys()):
                #por cada uno de estos...
                scope = Customlisteners.scopes[elem]
                
                #acceder a sus variables 
                for var in scope.symbolTable:
                    varObj = scope.symbolTable[var]
                    line = f'{elem}, {varObj.varType}, {varObj.name}, {varObj.offset}, {varObj.isArray}, {varObj.num}, {varObj.size} \n'
                    self.SymbolFile.write(line)


            self.SymbolFile.close()
            self.terminalSc.insert(tk.END, "Done. \n")
            tk.messagebox.showinfo(title="Successfully compiled!", message="No syntax errors found.")

            try:
                tk.messagebox.showinfo(title="CSV viewer", message="Using Libreoffice calc.")
                self.subprocess_cmd(f'{os.getcwd()}','kate .code.txt','libreoffice --calc symbols.csv')
                #self.child = subprocess.Popen([sys.executable, 'libreoffice --calc symbols.csv'])
                #os.system('libreoffice --calc symbols.csv')
            except:
                tk.messagebox.showerror(title="Couldn't launch csv viewer!", message="You can still check the file at ./symbols.csv")


        else:
            self.terminalSc.delete(1.0, tk.END)
            tk.messagebox.showerror(title="Compilation failed", message="Errors found, check the terminal")
            self.terminalSc.insert(tk.END, terminal)
            self.terminalSc.insert(tk.END, "[X] No errors found \n")
            self.terminalSc.insert(tk.END, "[X] Generated intermediate code \n")
            self.terminalSc.insert(tk.END, "[X] ARM code (to be implemented) \n")
            errs = "WARNING: Error(s) found while compilating! \n \n \n"
            for elem in Customlisteners.errors:
                errs += elem + '\n'
                print(elem)
            
            self.terminalSc.insert(tk.END, errs)



            


        
    def traverse(tree):
        if tree.getText() == "<EOF>":
            return None
        else:
            print(tree.getText())






if __name__ == '__main__':
    X = GUI()
    
