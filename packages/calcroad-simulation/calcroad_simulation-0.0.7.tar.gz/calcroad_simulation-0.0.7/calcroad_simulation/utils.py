from math import pi, cos, sin, asin

SIMULATION_START = 0
SIMULATION_END = 86400

GLOBAL_ACCEL = 2.94
GLOBAL_DECCEL = -2.94

def compute_dist(start, stop):
    """ballec
    R = 6378137  # rayon de la Terre en mètre
    start_rad = to_radian(start)
    stop_rad = to_radian(stop)
    print('startstop', start, stop)
    """
    return pow(
        pow(start[0]-stop[0], 2) 
        + pow(start[1]-stop[1], 2),
        0.5
    ) * 111277
    
    """useless
    print(
        R * (pi / 2 - asin(
        sin(stop_rad[0]) * sin(start_rad[0])
        + cos(stop_rad[1] - start_rad[1]) * cos(stop_rad[0]) * cos(start_rad[0])))
    )
    """

def to_radian(coord):
    return [(pi * coord[0]) / 180, (pi * coord[1]) / 180]

def get_vector(start, stop):
    lat_a, lon_a = start
    lat_b, lon_b = stop
    dist = compute_dist(start, stop)
    return [(lat_b - lat_a) / dist, (lon_b - lon_a) / dist]

