import uuid


class Road:
    def __init__(self, start_point, end_point, lanes=1, max_speed=50, id=None, name=None):
        self.id = uuid.uuid4().hex if id is None else id

        self.start_point = start_point
        self.end_point = end_point

        self.lanes = lanes
        self.max_speed = max_speed / 3.6
        self.name = name

    @property
    def length(self):
        return pow(
            pow(self.start_point[0] - self.end_point[0], 2)
            + pow(self.start_point[1] - self.end_point[1], 2), 0.5) * 111277  # THE Magic Constant

    @property
    def duration(self):
        return self.length / self.max_speed

    def distance(self, C):
        """
        Distance between this road and a given point
        """
        A, B = self.start_point, self.end_point
        L = self.length
        """(
            (self.end_point.x - self.start_point.x)**2
            + (self.end_point.y - self.start_point.y)**2
        )"""
        L2 = L*L
        r = ((C.x-A.x)*(B.x-A.x) + (C.y-A.y)*(B.y-A.y))/L2

        if r < 0:
            dcp = Road(A, C).length
        elif r > 1:
            dcp = Road(B, C).length
        else:
            s = ((A.y-C.y)*(B.x-A.x)-(A.x-C.x)*(B.y-A.y))/L
            dcp = abs(s)

        return dcp

    def __iter__(self):
        yield self.start_point
        yield self.end_point

    def __str__(self):
        return "(road %s)" % self.id

    def copy(self, p0, p1, id=False):
        data = self.dump()

        data['max_speed'] *= 3.6
        data['start_point'] = p0
        data['end_point'] = p1

        if not id:
            data.pop(id, None)

        return Road(**data)

    def dump(self):
        return {
            'id': self.id,
            'start_point': self.start_point,
            'end_point': self.end_point,
            'lanes': self.lanes,
            'max_speed': self.max_speed,
            'name': self.name
        }
