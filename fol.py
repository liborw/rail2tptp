

class Symbol(object):
    """Symbol of first order logic"""
    def __init__(self):
        super(Symbol, self).__init__()


class Function(Symbol):
    """Function symbol"""
    def __init__(self, identification, arguments):
        super(Function, self).__init__()
        if not type(identification) == list:
            self.identification = [identification]
        else:
            self.identification = identification
            
        if not type(arguments) == list:
            self.arguments = [arguments]
        else:
            self.arguments = arguments
    
    def __repr__(self):
        name = self.identification[0]
        args = ','.join(self.arguments)
        if len(self.identification) > 1:
            ids = '_'.join(self.ids[1:])
            function = "{0}_{1}({2})".format(name, ids, args)
        else:
            function = "{0}({1})".format(name, args)
        return function

class Predicate(Function):
    """Predicate symbol"""
    def __init__(self, identification, arguments, negation=None):
        super(Predicate, self).__init__(identification, arguments)
        self.negation = negation
    
    def __repr__(self):
        symbol = super(Predicate, self).__repr__()
        if self.negation:
            symbol = "~" + symbol
        return symbol

class Conectives(Symbol):
    """Conectives conjunction, disjunstion, implication, iff."""
    CONECTIVES = ('&', '|', '=>', '<=>')
    CONJ, DISJ, IMPL, IFF = CONECTIVES
    
    def __init__(self, conective):
        super(Conectives, self).__init__()
        self.conective = conective

class F(Function):
    """Shorthand for Function"""
    def __init__(self, *arg):
        super(F, self).__init__(*arg)

class P(Predicate):
    """Shorthand for Predicate"""
    def __init__(self, *arg):
        super(P, self).__init__(*arg)

class C(Conectives):
    """Shorthand for Connective"""
    def __init__(self, *arg):
        super(P, self).__init__(*arg)
    """docstring for C"""
    def __init__(self, arg):
        super(C, self).__init__()
        self.arg = arg

def disjunction(l):
    """Create compued """