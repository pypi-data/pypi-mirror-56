
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def copy(self):
        return Point(self.x, self.y)
