from .utils import DURATION
from .vehicule import Vehicule


class Journey:
    def __init__(self, start_time, max_vehicule, pathfinding=None):
        self.start_time = start_time
        self.pathfinding = pathfinding
        self.max_vehicules = max_vehicule
        self.timestamp_spawn = []

    def spawn_vehicule(self, timestamp):
        if timestamp in self.timestamp_spawn:
            vehicule = Vehicule(self.pathfinding)
            vehicule.initial_position()
            return vehicule
        return None

    def tick_spawn(self):
        delta = DURATION / 48
        tick = (2*delta) / (self.max_vehicules + 1)
        self.timestamp_spawn = [int((x*tick)+(self.start_time - delta))
                                for x in range(1, self.max_vehicules + 1)]
