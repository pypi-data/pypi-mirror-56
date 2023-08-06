from .road import Road


class Incident:
    def __init__(self, position, start, stop, speed, road):
        self.position = position
        self.start = start
        self.stop = stop
        self.speed = speed
        self.road: Road = road
        self.status = False

    def start_incident(self, timestamp):
        if self.start <= timestamp < self.stop and not self.status:
            self.status = True
            self.road.add_incident(self)

    def stop_incident(self, timestamp):
        if (self.start > timestamp or self.stop <= timestamp) and self.status == True:
            self.status = False
            self.road.del_incident(self)
