from .road import Road
from .incident import Incident
from .pathfinding import Pathfinding
from .journey import Journey
from .utils import DURATION


class Simulation:
    def __init__(self, roads=[], journeys=[], incidents=[]):
        self.set_roads(roads)
        self.set_incidents(incidents)
        self.set_journeys(journeys)

        self.vehicules = []
        self.time = 0

    def set_roads(self, roads=[]):
        self.roads = {}
        for road in roads:
            self.roads[road["id"]] = Road(start_point=road["start_point"],
                                          end_point=road["end_point"],
                                          max_speed=road["max_speed"] / 3.6,
                                          lanes=road["lanes"])

    def set_incidents(self, incidents=[]):
        self.incidents = []
        for incident in incidents:
            self.incidents.append(
                Incident(position=incident["position"],
                         start=incident["start"],
                         stop=incident["stop"],
                         speed=incident["speed"],
                         road=self.roads[incident["road"]]
                         )
            )

    def set_journeys(self, data_journeys=[]):
        self.journeys = []
        pathfinding = Pathfinding(self.roads)
        for data_journey in data_journeys:
            journey = Journey(
                data_journey["start_time"], data_journey["max_vehicule"])
            pathfinding_points = pathfinding.shortest_path(
                self.roads[data_journey["id_start"]].start_point,
                self.roads[data_journey["id_end"]].end_point
            )
            pathfinding_road = []
            for index_point in range(len(pathfinding_points) - 1):
                for road in self.roads:
                    if self.roads[road].start_point == pathfinding_points[index_point] and \
                            self.roads[road].end_point == pathfinding_points[index_point + 1]:
                        pathfinding_road.append(self.roads[road])
            journey.pathfinding = pathfinding_road
            journey.tick_spawn()
            self.journeys.append(journey)

    def run(self):
        with open("test.txt", "w+") as f:
            for timestamp in range(DURATION):
                to_destroy = []
                f.write(f't={timestamp}\n')
                # spawn vehicule
                for journey in self.journeys:
                    vehicule = journey.spawn_vehicule(timestamp)
                    if vehicule:
                        f.write(
                            f'spawn vehicule to position {vehicule.position}\n')
                        self.vehicules.append(vehicule)
                for incident in self.incidents:
                    incident.start_incident(timestamp)
                    incident.stop_incident(timestamp)
                for index, vehicule in enumerate(self.vehicules):
                    vehicule.next_position()
                    if vehicule.to_destroy:
                        to_destroy.append(vehicule)
                    else:
                        f.write(f'vehicule {vehicule} move to {vehicule.position}.'
                                f'current speed : {vehicule.speed},'
                                f'current movement : {vehicule.move_vector}\n')
                for vehicule in to_destroy:
                    self.vehicules.remove(vehicule)
