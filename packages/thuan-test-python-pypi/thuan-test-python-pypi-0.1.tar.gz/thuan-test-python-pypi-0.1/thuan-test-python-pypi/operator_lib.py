class Operator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def substract(self):
        return self.a - self.b
