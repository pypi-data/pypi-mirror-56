from math import pi, cos, sin, asin

DURATION = 1200
GLOBAL_ACCEL = 2.94
GLOBAL_DECCEL = -2.94

def compute_dist(start, stop):
    R = 6378137  # rayon de la Terre en mètre
    start_rad = to_radian(start)
    stop_rad = to_radian(stop)
    return R * (pi / 2 - asin(
        sin(stop_rad[0]) * sin(start_rad[0])
        + cos(stop_rad[1] - start_rad[1]) * cos(stop_rad[0]) * cos(start_rad[0])))

def to_radian(coord):
    return [(pi * coord[0]) / 180, (pi * coord[1]) / 180]

def get_vector(start, stop):
    lat_a, lon_a = start
    lat_b, lon_b = stop
    dist = compute_dist(start, stop)
    return [(lat_b - lat_a) / dist, (lon_b - lon_a) / dist]

