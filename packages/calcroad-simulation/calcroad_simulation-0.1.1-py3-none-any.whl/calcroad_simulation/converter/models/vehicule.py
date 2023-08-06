import uuid

from .functions import vector, distance
from .point import Point


class Vehicule:
    def __init__(self, simulation, path=[], max_speed=180, acceleration=2.7):
        self.simulation = simulation
        self.path = path

        self.speed = 0
        self.acceleration = acceleration
        self.max_speed = max_speed

        self.id = uuid.uuid4().hex
        self.road_index = -1
        self.next_road()

    def next_road(self):
        self.road_index += 1
        try:
            self.current_road = self.path[self.road_index]
            self.position = self.current_road.start_point.copy()
        except IndexError:
            self.simulation.drop_vehicule(self)

    def accelerate(self):
        self.speed = min(
            self.speed + self.acceleration,
            self.current_road.max_speed
        )

    def deccelerate(self):
        self.speed = max(
            0,
            self.speed - self.acceleration
        )

    def adapt_speed(self):
        if self.speed > self.current_road.max_speed:
            self.deccelerate()
        elif self.speed < self.current_road.max_speed:
            self.accelerate()

    def next_tick(self):
        self.adapt_speed()

        move = vector(self.current_road.start_point,
                      self.current_road.end_point)

        if distance(self.position, self.current_road.end_point) < self.speed:
            self.next_road()
            self.adapt_speed()
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
