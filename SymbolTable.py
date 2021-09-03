"""
Symbol Table:
{Entry.name: {...} }
"""
class SymbolTable():
    def __init__(self):
        self.scopes = ["global"]
        self.currentScope = self.scopes[0]
        self.parentScope = ""
        self.table = {self.currentScope: {}}

    def add_entry(self, entry) -> None:
        # self.isCorrect(entry)
        obj = {
            entry.id: entry
        }

        try:
            prevValues = {**self.table[self.currentScope]}
            self.table[self.currentScope] = prevValues | obj

        except KeyError:
            self.table[self.currentScope] = {
                entry.id: entry
            }

    def get_entry(self, entryQuery):
        try:
            return self.table[entryQuery["scope"]][hash(entryQuery["name"])]
        except KeyError:
            pass

    def get_scope(self, entryQuery):
        try:
            return self.table[entryQuery["scope"]]
        except KeyError:
            pass

    """
    entryQuery: {"scope": foo, "index": 1}
    """

    def get_entry_by_idx(self, entryQuery):
        try:
            variables = self.table[entryQuery["scope"]]
            keys = variables.keys()
            for elem in keys:
                if self.table[entryQuery["scope"]][elem].arrIndex == entryQuery["index"]:
                    return self.table[entryQuery["scope"]][elem]
        except KeyError:
            pass

    def update_entry(self, entry, typeNode) -> bool:
        if not self.checkTypeError(entry, typeNode):
            self.table[self.currentScope][entry.id] = entry
            return True
        else:
            return False

    def checkTypeError(self, entry, varType) -> bool:
        if entry.varType == varType:
            return False
        else:
            return True

    """
    Metodo utilizado para entrar a un nuevo ambito.
    """

    def nest_scope(self, newScope) -> None:
        self.scopes.append(newScope)
        self.parentScope = self.currentScope
        self.currentScope = newScope

    """
    Metodo utilizado para salir del ambito.
    """

    def exit_scope(self) -> None:
        self.scopes.pop()

        self.currentScope = self.scopes[len(self.scopes)-1]

        if len(self.scopes) >= 2:
            self.parentScope = self.scopes[len(self.scopes)-2]
        else:
            self.parentScope = "global"

    """
    Checks if the variable that is being added exists in a the same scope
    """

    def check_existing_same_scope(self, entry) -> bool:
        try:
            existingDictionary = self.table[entry.scope]
            existingDictionary[entry.id]
            return True

        except KeyError:

            return False


