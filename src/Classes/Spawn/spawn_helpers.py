from src.Utility.helpers.vector_helpers import distance


def is_valid_spawn_location(new_spawn, spawns):
    x, y, d = new_spawn.get_location_and_radius()
    for spawn in spawns:
        a, b, c = spawn.get_location_and_radius()
        tmp = distance((x, y), (a,b))
        if tmp < d or tmp < c:
            return False
    return True


def pretest_is_valid_spawn_location(new_point, points, d):
    for point in points:
        x, y = point[0], point[1]
        tmp = distance(new_point, (x, y))
        if tmp < d:
            return False
    return True
