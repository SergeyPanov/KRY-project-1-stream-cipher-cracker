class Term:
    def __init__(self, name, is_negated = False, value = None):
        self.name = name
        self.is_negated = is_negated
        self.value = value

    def negate(self):
        self.is_negated = not self.is_negated

    def getValue(self):
        if self.value != None:
            if self.is_negated:
                return not self.value
        return self.value

    def assignValue(self, value):
        self.value = value