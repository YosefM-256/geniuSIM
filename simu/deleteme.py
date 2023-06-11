class a():
    def __init__(self):
        self.t = 1
        print("a created")

class b(a):
    def __init__(self):
        self.y = 3
        a.__init__(self)
