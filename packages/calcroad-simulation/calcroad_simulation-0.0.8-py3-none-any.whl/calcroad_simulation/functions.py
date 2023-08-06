
def distance(p0, p1):
    return pow(
        pow(p0.x-p1.x, 2) + pow(p0.y-p1.y, 2),
        0.5
    ) * 111277


def vector(p0, p1):
    d = distance(p0, p1)
    return [(p1.x - p0.x) / d, (p1.y - p0.y) / d]
