from logic.Term import Term


class Clause:

    def __init__(self, least, number, is_negated = False, operator = 'and'):
        self.operator = operator
        self.terms = []
        self.number = number
        self.is_negated = is_negated

        self.terms.append(Term("x"+str(least + 2), (4 & number) == 0))
        self.terms.append(Term("x"+str(least + 1), (2 & number) == 0))
        self.terms.append(Term("x"+str(least), (1 & number) == 0))

    def negate(self):
        [term.negate() for term in self.terms]
        if self.operator == 'and':
            self.operator = 'or'
        else:
            self.operator = 'and'

    def deMorgan(self):
        self.negate()

    def apply(self, left, mid):
        self.terms[0].assignValue(left)
        self.terms[1].assignValue(mid)

    def simplify(self):
        self.simplifyed_value = self.terms[2]
        for term in self.terms:
            if term.getValue() == True:
                self.simplifyed_value = Term("value", value=True)

    def getSimplifyed(self):
        return self.simplifyed_value