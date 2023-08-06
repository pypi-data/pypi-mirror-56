from .road import Road
from .incident import Incident
from .pathfinding import Pathfinding
from .journey import Journey
from .utils import DURATION


class Simulation:
    def __init__(self, roads=[], journeys=[], incidents=[], db_session=None, position_model=None, debug=False):
        self.set_roads(roads)
        self.set_incidents(incidents)
        self.set_journeys(journeys)
        
        # attribute for log in database
        self.config_database(db_session, position_model)

        self.debug = debug
        if self.debug:
            open('test.txt', 'w').close()
            self.log_file = open('test.txt', 'a')
        
        self.vehicules = []
        self.time = 0
        
        
    def config_database(self, db_session, position_model):
        if db_session is not None and position_model is None:
            raise ValueError('Missing VehiculePosition model')
        
        self.db_session = db_session
        self.position_model = position_model

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
            
    def log(self, text):
        if self.debug:
            self.log_file.write(text+'\n')

    def run(self):            
        for timestamp in range(DURATION):
            to_destroy = []
            self.log(f't={timestamp}')
            # spawn vehicule
            for journey in self.journeys:
                vehicule = journey.spawn_vehicule(timestamp)
                if vehicule:
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
            
            if self.db_session is not None:
                self.db_session.add_all([self.position_model(**vehicule.json()) for vehicule in self.vehicules])
        
        if self.db_session:
            db_session.commit()
        