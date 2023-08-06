from collections import namedtuple, defaultdict
from random import randint
import uuid
from dijkstar import find_path
from ..functions import distance, vector

from .road import Road


def unique_id():
    return uuid.uuid4().hex


class Vehicule:
    def __init__(self, simulation, path=[], max_speed=180):
        self.simulation = simulation
        self.path = path

        self.id = unique_id()
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


class Journey:
    def __init__(self, simulation, start_point, end_point, start_time, id_start, id_end, max_vehicules):
        self.set_simulation(simulation)

        self.id = unique_id()
        self.start_point = start_point
        self.end_point = end_point
        self.start_time = start_time

        self.id_start = id_start
        self.id_end = id_end
        self.max_vehicules = max_vehicules

        self.vehicules_to_spawn = defaultdict(list)

    def set_simulation(self, simulation):
        self.simulation = simulation
        self.graph = simulation.graph

    def workout_path(self, roads_by_points):
        nodes = find_path(
            self.graph,
            self.start_point,
            self.end_point
        ).nodes

        path = []
        for k in range(len(nodes)-1):
            road = roads_by_points[(nodes[k], nodes[k+1])]
            path.append(road.copy(nodes[k], nodes[k+1], id=True))

        for _ in range(self.max_vehicules):
            self.vehicules_to_spawn[self.start_time + randint(0, 45)].append(
                Vehicule(self.simulation, path)
            )

    def spawns(self, timestamp):
        return self.vehicules_to_spawn[timestamp]

    """def dump(self):
        return {
            "id": self.id,
            "start_point": self.start_point,
            "end_point": self.end_point,
            "start_time": self.start_time,
            "id_start": self.id_start,
            "id_end": self.id_end,
            "max_vehicules": self.max_vehicules
        }"""


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
