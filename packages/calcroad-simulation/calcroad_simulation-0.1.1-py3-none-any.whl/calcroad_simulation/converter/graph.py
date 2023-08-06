from .models import Point

COLINEAR = 'COLINEAR'


class GraphMaker:
    def __init__(self):
        self._roads = []
        self._journeys = []

    def intersection(self, segment1, segment2):
        p0, p1 = segment1
        p2, p3 = segment2

        #        I        x        J
        d = (p1.x - p0.x) * (p3.y - p2.y) - \
            (p1.y - p0.y) * (p3.x - p2.x)

        if d == 0:
            return COLINEAR

        m = ((p1.x - p0.x) * (p0.y - p2.y) - (p1.y - p0.y) * (p0.x - p2.x)) / d
        n = ((p3.x - p2.x) * (p0.y - p2.y) - (p3.y - p2.y) * (p0.x - p2.x)) / d

        if m < 0 or m > 1 or n < 0 or n > 1:
            return None

        I = Point(p2.x + m*(p3.x - p2.x), p2.y + m*(p3.y - p2.y))
        if I != p2 and I != p3:
            return I

        return None

    def find_intersections(self, _segment):
        intersections = []
        for segment in self._roads:
            intersection = self.intersection(segment, _segment)
            if intersection and intersection is not COLINEAR:
                intersections.append((intersection, segment))
        return intersections

    def add_road(self, _segment):
        if _segment.length == 0:
            return

        intersections = self.find_intersections(_segment)
        if len(intersections)>0:
            i, segment = intersections[0] 
            subroads = self.create_intersection(segment, _segment, i)
            self.remove_road(segment)
            for subsegment in subroads:
                self.add_road(subsegment)
        else:
            self._roads.append(_segment)

    def create_intersection(self, road1, road2, i):
        subroads = [
            road1.copy(road1.start_point, i),
            road1.copy(i, road1.end_point),
            road2.copy(road2.start_point, i),
            road2.copy(i, road2.end_point)
        ]
        return tuple(filter(lambda segment: segment.length > 0, subroads))

    def remove_road(self, road):
        try:
            self._roads.remove(road)
        except ValueError:
            pass

    def closest_road(self, p):
        i = min(
            enumerate(self._roads),
            key=lambda item: item[1].distance(p)
        )[0]
        return self._roads[i]

    def add_journey(self, journey):
        self._journeys.append(journey)

    @property
    def roads(self):
        return [road.dump() for road in self._roads]

    @property
    def journeys(self):
        return [journey.dump() for journey in self._journeys]
