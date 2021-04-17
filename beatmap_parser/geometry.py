import math


def norm(i, j):
    scale = math.hypot(i, j)
    return i / scale, j / scale


def collinear(p1, p2, p3):
    x1, y1, x2, y2, x3, y3 = p1 + p2 + p3
    return x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2) == 0


def define_circle(p1, p2, p3):
    x, y, z = [complex(*p) for p in (p1, p2, p3)]
    w = z-x
    w /= y-x
    c = (x-y)*(w-abs(w)**2)/2j/w.imag-x

    return (-c.real, -c.imag), abs(c+x)


def rotate(xo, yo, x, y, theta):
    xr = math.cos(theta)*(x-xo)-math.sin(theta)*(y-yo) + xo
    yr = math.sin(theta)*(x-xo)+math.cos(theta)*(y-yo) + yo
    return xr, yr


def is_left(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) < 0


def points_equal(p1, p2):
    return p1[0] == p2[0] and p1[1] == p2[1]
