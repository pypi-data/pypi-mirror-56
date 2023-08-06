from .converter import MapConverter
from .settings import SimulatorSettings

from dijkstar import Graph, find_path
from collections import defaultdict


class Simulation:
    def __init__(self, map):
        self.map_id = int(map.id)
        self.graph = Graph()
        converter = MapConverter(self, map)

        self.roads = converter.roads
        self.roads_by_id = dict((road.id, road) for road in converter.roads)
        self.journeys = converter.journeys
        self.points = self.get_points(converter.roads)
        self.vehicules = []

    def get_points(self, roads):
        points = set()
        for road in roads:
            points.add(road.start_point)
            points.add(road.end_point)
        return tuple(points)

    def generate_graph(self):
        for index in self.points:
            self.graph.add_node(index)

        for road in self.roads:
            i = road.start_point
            j = road.end_point
            self.graph.add_edge(i, j, road.duration)
            self.graph.add_edge(j, i, road.duration)

        return self.graph

    def drop_vehicule(self, vehicule):
        self.vehicules.remove(vehicule)

    def get_road_by_path(self):
        roads_by_path = {}
        for road in self.roads:
            roads_by_path[(road.start_point, road.end_point)] = road
            roads_by_path[(road.end_point, road.start_point)] = road
        return roads_by_path

    def run(self):
        self.generate_graph()

        roads_by_path = self.get_road_by_path()

        vehicules_to_spawn = defaultdict(list)
        for journey in self.journeys:
            journey.workout_path(roads_by_path)
            for timestamp, vehicules in journey.vehicules_to_spawn.items():
                vehicules_to_spawn[timestamp].extend(vehicules)

        for timestamp in range(0, 86400):
            self.vehicules.extend(vehicules_to_spawn[timestamp])
            for vehicule in self.vehicules:
                vehicule.next_tick()

            if SimulatorSettings.db_session is not None:
                SimulatorSettings.db_session.add_all([
                    SimulatorSettings.position_model(
                        map_id=self.map_id,
                        time=timestamp,
                        **vehicule.json()
                    )
                    for vehicule in self.vehicules
                ])

        if SimulatorSettings.db_session is not None:
            SimulatorSettings.db_session.commit()
