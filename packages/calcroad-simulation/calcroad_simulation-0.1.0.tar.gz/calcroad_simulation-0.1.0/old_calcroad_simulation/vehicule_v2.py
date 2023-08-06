from .road import Road
from .utils import get_vector, compute_dist, GLOBAL_ACCEL, GLOBAL_DECCEL


class Vehicule:
    def __init__(self, pathfinding, max_speed=130):
        self.current_road: Road = pathfinding[0]
        self.speed = 0.0
        self.max_speed = max_speed
        self.current_accel = 0
        self.pathfinding: [Road] = pathfinding
        self.position = []
        self.initial_position()
        self.move_vector = get_vector(
            self.current_road.start_point, self.current_road.end_point)
        self.to_destroy = False

    def initial_position(self):
        lat_a, lon_a = self.current_road.start_point
        lat_b, lon_b = self.current_road.end_point
        lat_start = (lat_b + lat_a) / 2
        lon_start = (lon_b + lon_a) / 2
        self.position = [lat_start, lon_start]

    def acceleration(self, limit):
        if limit > self.current_road.max_speed:
            limit = self.current_road.max_speed
        if self.speed < limit and (limit - self.speed) > GLOBAL_ACCEL:
            self.speed += GLOBAL_ACCEL
        elif self.speed < limit and (limit - self.speed) <= GLOBAL_ACCEL:
            self.speed = limit
        else:
            pass

    def decceleration(self, limit):
        if self.speed > limit and (limit - self.speed) < GLOBAL_DECCEL:
            self.speed += GLOBAL_DECCEL
        elif self.speed > limit and (limit - self.speed) <= GLOBAL_DECCEL:
            self.speed = limit
        else:
            pass

    def emergency_decceleration(self, element):
        dist_to_element = compute_dist(self.position, element.position)
        deccel = 2 * (dist_to_element - self.speed - 1)
        if deccel >= (self.speed - element.speed):
            self.speed = element.speed
        else:
            self.speed -= deccel

    def get_closest(self, e1, e2):
        if compute_dist(self.position, e1.position) < compute_dist(self.position, e2.position):
            return e1
        return e2

    def get_element_toward(self):
        toward = None
        self_to_end = compute_dist(self.position, self.current_road.end_point)
        for element in self.current_road.elements:
            if element is not self and self_to_end > compute_dist(element.position, self.current_road.end_point):
                if not toward:
                    toward = element
                else:
                    self.get_closest(toward, element)
        return toward

    def going_to_next_road(self):
        if len(self.pathfinding) >= self.pathfinding.index(self.current_road):
            return False
        dist_to_next = compute_dist(self.position, self.current_road.end_point)
        if self.speed >= dist_to_next:
            return True
        return False

    def next_position(self):
        # increment position
        if not self.to_destroy:
            next_point_dist = compute_dist(
                self.position, self.current_road.end_point)
            if next_point_dist <= self.speed:
                self.position = self.current_road.end_point
                self.current_road.elements.remove(self)
                self.current_road = self.pathfinding[self.pathfinding.index(
                    self.current_road) + 1]
                self.current_road.elements.append(self)
                dist_to_travel = self.speed - next_point_dist
                self.move_vector = get_vector(
                    self.current_road.start_point, self.current_road.end_point)
            else:
                dist_to_travel = self.speed

            next_lat = self.position[0] + \
                (self.move_vector[0] * dist_to_travel)
            next_lon = self.position[1] + \
                (self.move_vector[1] * dist_to_travel)
            self.position = [next_lat, next_lon]

        toward = self.get_element_toward()

        if not toward and not self.going_to_next_road():
            if self.speed < self.current_road.max_speed:
                self.acceleration(self.current_road.max_speed)
            else:
                self.decceleration(self.current_road.max_speed)

        if toward:
            dist_to_toward = compute_dist(self.position, toward.position)
            stop_time = - self.speed / GLOBAL_DECCEL
            stop_distance = 1 / 2 * GLOBAL_DECCEL * \
                (stop_time * stop_time) + self.speed * stop_time
            if type(toward) is Vehicule:
                if toward.speed > self.speed and dist_to_toward > stop_distance:
                    self.acceleration(self.current_road.max_speed)
                elif toward.speed > self.speed and dist_to_toward < stop_distance:
                    self.acceleration(toward.speed)
                else:
                    if dist_to_toward < stop_distance:
                        self.emergency_decceleration(toward)
                    elif stop_distance < dist_to_toward <= (2 * stop_distance):
                        self.decceleration(toward.speed)
                    else:
                        self.acceleration(self.current_road.max_speed)
            else:
                if toward.speed > self.speed and dist_to_toward > stop_distance:
                    self.acceleration(self.current_road.max_speed)
                elif toward.speed > self.speed and dist_to_toward < stop_distance:
                    self.acceleration(toward.speed)
                else:
                    if dist_to_toward < stop_distance and toward.speed == 0:
                        self.emergency_decceleration(toward)
                    elif dist_to_toward < stop_distance and toward.speed != 0:
                        self.decceleration(toward.speed)
                    elif stop_distance < dist_to_toward <= (2 * stop_distance):
                        self.decceleration(toward.speed)
                    else:
                        self.acceleration(self.current_road.max_speed)

        if self.going_to_next_road():
            next_road = self.pathfinding[self.pathfinding.index(
                self.current_road) + 1]
            if next_road.max_speed < self.speed:
                self.decceleration(next_road.max_speed)

        if self.current_road is self.pathfinding[-1]:
            lat_a, lon_a = self.current_road.start_point
            lat_b, lon_b = self.current_road.end_point
            lat_mid = (lat_b + lat_a) / 2
            lon_mid = (lon_b + lon_a) / 2
            end_point = [lat_mid, lon_mid]
            dist_to_end = compute_dist(self.position, end_point)
            stop_time = - self.speed / GLOBAL_DECCEL
            stop_distance = 1 / 2 * GLOBAL_DECCEL * \
                (stop_time * stop_time) + self.speed * stop_time
            if stop_distance > dist_to_end and dist_to_end > 1:
                self.decceleration(0)
            else:
                self.speed = 0.0
                self.to_destroy = True
                self.current_road.elements.remove(self)
