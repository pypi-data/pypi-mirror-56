from .road import Road
from .incident import Incident
from .pathfinding import Pathfinding
from .journey import Journey
from .settings import SimulatorSettings
from .utils import SIMULATION_START, SIMULATION_END


class Simulation:
    def __init__(self, map_id, roads=[], journeys=[], incidents=[], debug=False):
        self.map_id = map_id
        
        self.set_roads(roads)
        self.set_incidents(incidents)
        self.set_journeys(journeys)

        self.debug = debug
        if self.debug:
            open('test.txt', 'w').close()
            self.log_file = open('test.txt', 'a')
        
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
            
            journey = Journey(
                **data_journey,
                pathfinding = pathfinding_road
            )
            
            self.journeys.append(journey)
            
    def log(self, text):
        if self.debug:
            self.log_file.write(text+'\n')

    def run(self):   
        if SimulatorSettings.db_session is not None and SimulatorSettings.position_model is None:
            raise ValueError('Missing VehiculePosition model')
        
        # TODO: optimise in function of journeys start_time
        for timestamp in range(SIMULATION_START, SIMULATION_END):
            to_destroy = []
            self.log(f't={timestamp}')
            # spawn vehicule
            for journey in self.journeys:
                if timestamp == journey.start_time:
                    for _ in range(journey.max_vehicules):
                        vehicule = journey.spawn_vehicule(timestamp)
                        self.log(f'[spawn vehicule] {vehicule.json()}')
                        self.vehicules.append(vehicule)
                    
            for incident in self.incidents:
                incident.start_incident(timestamp)
                incident.stop_incident(timestamp)
                
            for index, vehicule in enumerate(self.vehicules):
                vehicule.next_position()
                if vehicule.to_destroy:
                    to_destroy.append(vehicule)
                else:
                    self.log(f'[move vehicule] {vehicule.json()}')
            
            for vehicule in to_destroy:
                self.vehicules.remove(vehicule)
            
            if SimulatorSettings.db_session is not None:
                SimulatorSettings.db_session.add_all([
                    SimulatorSettings.position_model(
                        map_id=self.map_id,
                        time=timestamp, 
                        **vehicule.json()
                    ) 
                    for vehicule in self.vehicules
                ])
        
        if SimulatorSettings.db_session:
            SimulatorSettings.db_session.commit()
        