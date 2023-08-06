from .models import Point, Road, Journey
from .graph import GraphMaker


class MapConverter:
    def __init__(self, simulation, map):
        self.map = map
        self.simulation = simulation
        self.graph = GraphMaker()
        self.convert()

    def split_roads(self):
        for road in self.map.roads:
            points = road.coordinates

            for k in range(len(points)-1):
                child_road = Road(
                    Point(points[k].lng, points[k].lat),
                    Point(points[k+1].lng, points[k+1].lat),
                    lanes=road.lanes,
                    max_speed=road.max_speed,
                    name=road.name
                )
                self.graph.add_road(child_road)

    def bind_journeys_roads(self):
        journeys = self.map.journeys

        for journey in journeys:
            p0 = Point(journey.start_point.lng, journey.start_point.lat)
            p1 = Point(journey.end_point.lng, journey.end_point.lat)

            road0 = self.graph.closest_road(p0)
            road1 = self.graph.closest_road(p1)

            self.graph.remove_road(road0)
            self.graph.remove_road(road1)

            self.graph.add_road(road0.copy(road0.start_point, p0))
            self.graph.add_road(road0.copy(p0, road0.end_point))
            self.graph.add_road(road1.copy(road1.start_point, p1))
            self.graph.add_road(road1.copy(p1, road1.end_point))

            self.graph.add_journey(
                Journey(self.simulation, p0, p1,
                        journey.start_time, journey.max_vehicules)
            )

    def convert(self):
        self.split_roads()
        self.bind_journeys_roads()

    @property
    def roads(self):
        return self.graph._roads

    @property
    def journeys(self):
        return self.graph._journeys
