from .vehicule import Vehicule


class Journey:
    def __init__(self, start_time, max_vehicules, pathfinding=None, **kwargs):
        self.start_time = start_time
        self.pathfinding = pathfinding
        self.max_vehicules = max_vehicules

    def spawn_vehicule(self, timestamp):
        vehicule = Vehicule(self.pathfinding)
        vehicule.initial_position()
        return vehicule
