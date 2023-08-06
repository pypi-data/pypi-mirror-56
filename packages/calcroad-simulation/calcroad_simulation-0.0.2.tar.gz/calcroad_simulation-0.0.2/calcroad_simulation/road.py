class Road:
    def __init__(self, start_point, end_point, max_speed, lanes):
        self.start_point = start_point
        self.end_point = end_point
        self.max_speed = max_speed
        self.lanes = lanes
        self.elements = []

    def add_incident(self, incident):
         self.elements.append(incident)

    def del_incident(self, incident):
        self.elements.remove(incident)

    def add_vehicule(self, vehicule):
        self.elements.append(vehicule)

    def del_vehicule(self, vehicule):
        self.elements.remove(vehicule)