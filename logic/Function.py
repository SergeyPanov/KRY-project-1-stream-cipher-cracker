class Function:
    def __init__(self, clauses, operator = 'and', is_negated = False):
        self.clauses = clauses
        self.is_negated = is_negated
        self.operator = operator

    def apply(self, left, mid):
        [clause.apply(left, mid) for clause in self.clauses]

    def simplify(self):
        [clause.simplify() for clause in self.clauses]

        for clause in self.clauses:
            if clause.simplifyed_value.getValue() == False:
                self.simplifyed_value = False
            if clause.simplifyed_value.getValue() == None:
                self.simplifyed_value = clause.simplifyed_value
