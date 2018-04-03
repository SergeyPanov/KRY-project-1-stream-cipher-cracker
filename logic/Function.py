class Function:
    def __init__(self, clauses, operator = 'and', is_negated = False):
        self.clauses = clauses
        self.is_negated = is_negated
        self.operator = operator
