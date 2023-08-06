from math import inf
from .utils import compute_dist


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
        for road in roads:
            dist = compute_dist(roads[road].start_point, roads[road].end_point)
            time = dist / roads[road].max_speed
            x = self.points.index(roads[road].start_point)
            y = self.points.index(roads[road].end_point)
            self.matrix[x][y] = time

    def shortest_path(self, start_point, end_point):
        start = self.points.index(start_point)
        end = self.points.index(end_point)
        return self.dijkstra(start, end)

    def dijkstra(self, init, dest):
        unvisited_nodes = [x for x in range(len(self.points))]
        administrative_distance = [inf for _ in range(len(self.points))]
        administrative_distance[init] = 0
        previous_neighbour = [-1 for _ in range(len(self.points))]
        current_node = init
        while administrative_distance[current_node] is not inf and current_node != dest:
            unvisited_nodes.remove(current_node)
            for neighbour_index, neighbour_dist in enumerate(self.matrix[current_node]):
                if neighbour_index in unvisited_nodes and neighbour_dist is not inf and current_node != neighbour_index:
                    alt = neighbour_dist + \
                        administrative_distance[current_node]
                    if alt < administrative_distance[neighbour_index]:
                        administrative_distance[neighbour_index] = alt
                        previous_neighbour[neighbour_index] = current_node
            current_node = unvisited_nodes[0]
            for node in unvisited_nodes:
                if administrative_distance[node] < administrative_distance[current_node]:
                    current_node = node
        if administrative_distance[dest] is not inf:
            shortest_path = [dest]
            path_points = []
            previous = dest
            while previous_neighbour[previous] != -1:
                previous = previous_neighbour[previous]
                shortest_path.append(previous)
            for node in list(reversed(shortest_path)):
                path_points.append(self.points[node])
            return path_points
        else:
            return None
