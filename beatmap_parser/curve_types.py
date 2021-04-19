from abc import ABC, abstractmethod
import bezier
import numpy as np

from .geometry import *


class Curve(ABC):
    def __init__(self, points):
        self.points = points
    
    
    @classmethod
    def split(self, points):
        ret = [[points[0]]] if len(points) else []
        
        for i in range(1, len(points)):
            if points_equal(points[i], ret[-1][-1]):
                ret.append([])
            ret[-1].append(points[i])
        
        return ret


    @abstractmethod
    def endpoint(self, length):
        pass


class Bezier(Curve):

    def __init__(self, points):
        super().__init__(points)

        degree = len(self.points) - 1
        self.curve = bezier.Curve(np.asarray(self.points).T, degree)

    def endpoint(self, length):
        
        diff = length - self.curve.length

        if diff > 0:
            x_end, y_end = self.points[-1]

            tan_vec = self.curve.evaluate_hodograph(.999).flatten()
            i, j = norm(*tan_vec)

            return x_end + diff * i, y_end + diff * j

        return self.curve.evaluate(length / self.curve.length).flatten()


class Linear(Curve):

    def endpoint(self, length):
        
        x, y, x1, y1 = np.asarray(self.points[:2]).flatten()
        i, j = norm(x1 - x, y1 - y)

        return x + length * i, y + length * j


class PerfectCircle(Curve):

    def endpoint(self, length):
        
        center, radius = define_circle(*self.points)

        radians = length / radius

        if is_left(*self.points):
            radians *= -1

        return rotate(*center, *self.points[0], radians)


curve_types = {
    'B': Bezier,
    'L': Linear,
    'P': PerfectCircle
}


def resolve_curve_type(curve_type, points):
    n_points = len(points)

    if curve_type == 'C' or n_points < 2:
        return None
    elif n_points == 2:
        return Linear
    elif n_points == 3:
        if collinear(*points):
            points = points[:2]
            return Linear
    elif n_points > 3:
        return Bezier

    return curve_types[curve_type]
