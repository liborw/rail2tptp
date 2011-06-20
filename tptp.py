def fof(name, role, formula, annotaion=None):
    """Create fof formula in TPTP format"""
    return "fof({0}, {1}, {2}).".format(name, role, formula)