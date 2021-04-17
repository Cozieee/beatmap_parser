from .definitions import s_int
from .curve_types import resolve_curve_type
from .geometry import points_equal


def hitobject_default(s):
    return tuple(map(s_int, s.split(",")[:3]))


def curve_point(s):
    return tuple(map(s_int, s.split(":")))


def curve_data(s):
    curve_data = s.split("|")

    curve_type = curve_data[0]
    curve_points = map(curve_point, curve_data[1:])

    return curve_type, list(curve_points)


def slider(s, timing_point):
    x, y, time = hitobject_default(s)

    vals = s.split(",")
    curve_type, curve_points = curve_data(vals[5])
    repeat_count, px_length = s_int(vals[6]), float(vals[7])

    if not (len(curve_points) and points_equal((x, y), curve_points[0])):
        curve_points = [(x, y)] + curve_points

    curve_class = resolve_curve_type(curve_type, curve_points)

    x1, y1 = curve_class(curve_points).endpoint(
        px_length) if curve_class and len(curve_points) < 100 else curve_points[-1]

    px_per_ms = timing_point[1]
    duration = int(px_length / px_per_ms)

    return int(x1), int(y1), duration, repeat_count