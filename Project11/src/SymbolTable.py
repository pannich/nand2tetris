class SymbolTable:
    # hash table { 'name' : (type, kind, index) }

    def __init__(self):
        self.counts             = {}
        self.counts['FIELD']    = 0
        self.counts['STATIC']   = 0

        self.subroutine_scope   = {}
        self.class_scope        = {}

    def startSubroutine(self):
        """Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s scope.)"""
        self.subroutine_scope = {}
        self.counts['ARG']    = 0       # starts from 0
        self.counts['VAR']    = 0

    def define(self, name, type, kind):
        """
        name (String)
        type (string)
        kind (STATIC, FIELD, ARG, or VAR)
        """
        index = None

        # subroutine scope ARG, VAR
        if kind in ('ARG', 'VAR'):
            if kind == 'ARG':
                index = self.counts['ARG']
                self.counts['ARG'] += 1         # increment for next
            elif kind == 'VAR':
                index = self.counts['VAR']
                self.counts['VAR'] += 1

            self.subroutine_scope[name] = (type, kind, index)

        elif kind in ('STATIC', 'FIELD'):
            if kind == 'STATIC':
                index = self.counts['STATIC']
                self.counts['STATIC'] += 1

            elif kind == 'FIELD':
                index = self.counts['FIELD']
                self.counts['FIELD'] += 1

            self.class_scope[name] = (type, kind, index)    # add new symbol to dict

    def varCount(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current scope.

        Args : kind (STATIC, FIELD, ARG, or VAR)
        return : int
        """
        return self.counts[kind]     # we already count it

    def kindOf(self, name):
        """
        Returns the kind of the named identifier in the current scope. Returns NONE if the identifier is unknown in the current scope.
        Args    : name
        return  : (STATIC, FIELD, ARG, VAR, NONE)
        """
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][1]
        elif name in self.class_scope:
            return self.class_scope[name][1]
        else:
            return None

    def typeOf(self, name):
        """
        Returns the type of the named identifier in the current scope.
        Args    : name
        return  : type(__String__)
        """
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][0]
        elif name in self.class_scope:
            return self.class_scope[name][0]
        else:
            return None

    def indexOf(self, name):
        """
        Returns the index of the named identifier in the current scope.
        Args    : name
        return  : index(__String__)
        """
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][2]
        elif name in self.class_scope:
            return self.class_scope[name][2]
        else:
            return None
