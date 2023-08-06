from math import inf
from .utils import compute_dist
from .exceptions import PathNotFound


class Pathfinding():
    def __init__(self,  roads):
        self.points = []
        self.set_points(roads)
        self.matrix = [[inf for _ in range(len(self.points))]
                       for _ in range(len(self.points))]
        self.set_matrix(roads)

    def set_points(self, roads):
        for road in roads:
            if roads[road].start_point not in self.points:
                self.points.append(roads[road].start_point)
            if roads[road].end_point not in self.points:
                self.points.append(roads[road].end_point)

    def set_matrix(self, roads):
        from dijkstar import Graph
        self.graph = Graph()
        for k in range(len(self.points)):
            self.graph.add_node(k)

        for road in roads:
            dist = compute_dist(roads[road].start_point, roads[road].end_point)
            time = dist / roads[road].max_speed
            x = self.points.index(roads[road].start_point)
            y = self.points.index(roads[road].end_point)
            self.graph.add_edge(x, y, time)
            self.graph.add_edge(y, x, time)
        print(self.graph)

    def shortest_path(self, start_point, end_point):
        from dijkstar import find_path
        start = self.points.index(start_point)
        end = self.points.index(end_point)
        path = find_path(self.graph, start, end).nodes
        pathfinding = [self.points[node] for node in path]
        print('pathfinding', pathfinding)
        return pathfinding
