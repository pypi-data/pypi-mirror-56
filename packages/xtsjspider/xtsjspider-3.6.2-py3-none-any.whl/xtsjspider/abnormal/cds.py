class A:
    a = 1

    def ass(self, b):
        print(b)

    def pars(self):
        getattr(self, "ass")(2)



b = A()
b.pars()