from collections import defaultdict
from random import randint
from dijkstar import find_path

from .functions import unique_id
from .vehicule import Vehicule


class Journey:
    def __init__(self, simulation, start_point, end_point, start_time, max_vehicules):
        self.set_simulation(simulation)

        self.id = unique_id()
        self.start_point = start_point
        self.end_point = end_point
        self.start_time = start_time
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
