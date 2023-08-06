import uuid

from .functions import vector, distance
from .point import Point


class Vehicule:
    def __init__(self, simulation, path=[], max_speed=180):
        self.simulation = simulation
        self.path = path

        self.id = uuid.uuid4().hex
        self.road_index = -1
        self.next_road()

    def next_road(self):
        self.road_index += 1
        try:
            self.current_road = self.path[self.road_index]
            self.position = self.current_road.start_point.copy()
            self.speed = self.current_road.max_speed
        except IndexError:
            self.simulation.drop_vehicule(self)

    def next_tick(self):
        move = vector(self.current_road.start_point,
                      self.current_road.end_point)

        if distance(self.position, self.current_road.end_point) < self.speed:
            self.next_road()
        else:
            self.position = Point(
                self.position.x + move[0] * self.speed,
                self.position.y + move[1] * self.speed
            )

    def json(self):
        return {
            "id": self.id,
            "speed": self.speed,
            "lat": self.position.x,
            "lng": self.position.y
        }
