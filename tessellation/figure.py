from functools import reduce
import operator
import math
import numpy as np
import matplotlib.pyplot as plt

from tessellation.utils import angle, rotate_around_the_point

class Figure:
    def __init__(self, vertices: list):
        self.vertices = vertices
        self.area: float
        self.bounds: dict
        self.left_top_point: float
        self.right_top_point: float
        self.right_bottom_point: float
        self.left_bottom_point: float

        self.sort_vertices()

    def sort_vertices(self):
        n = len(self.vertices)
        cx = float(sum(x for x, y in self.vertices)) / n
        cy = float(sum(y for x, y in self.vertices)) / n
        vertices_with_angles = []
        for x, y in self.vertices:
            an = (np.arctan2(y - cy, x - cx) + 2.0 * np.pi) % (2.0 * np.pi)
            vertices_with_angles.append((x, y, an))
        vertices_with_angles.sort(key = lambda tup: tup[2])
        self.vertices = [(x, y) for x, y, _ in vertices_with_angles]

    def calc_bounds(self):
        self.bounds = {
            "left": float("inf"),
            "right": float("-inf"),
            "bottom": float("inf"),
            "top": float("-inf")
        }
        self.bounds_index = {
            "left": int,
            "right": int,
            "bottom": int,
            "top": int
        }

        for it, vertex in enumerate(self.vertices):
            if vertex[0] < self.bounds['left']:
                self.bounds['left'] = vertex[0]
                self.bounds_index['left'] = it
            if vertex[0] > self.bounds['right']:
                self.bounds['right'] = vertex[0]
                self.bounds_index['right'] = it
            if vertex[1] < self.bounds['bottom']:
                self.bounds['bottom'] = vertex[1]
                self.bounds_index['bottom'] = it
            if vertex[1] > self.bounds['top']:
                self.bounds['top'] = vertex[1]
                self.bounds_index['top'] = it

    def order_points(self):
        center = tuple(
            map(
                operator.truediv,
                reduce(lambda x, y: map(operator.add, x, y), self.vertices),
                [len(self.vertices)] * 2
                )
        )
        ordered = sorted(
            self.vertices,
            key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360
        )

        max_y = float("-inf")
        max_y_it: int
        for it, point in enumerate(ordered):
            if point[1] > max_y:
                max_y = point[1]
                max_y_it = it
            elif point[1] == max_y:
                if point[0] > ordered[max_y_it][0]:
                    max_y_it = it

        if ordered[max_y_it - 1][0] < ordered[max_y_it][0]:
            self.right_top_point = ordered[max_y_it]
            self.left_top_point = ordered[max_y_it - 1]
            self.left_bottom_point = ordered[max_y_it - 2]
            self.right_bottom_point = ordered[max_y_it - 3]
        else:
            self.left_top_point = ordered[max_y_it]
            self.left_bottom_point = ordered[max_y_it - 1]
            self.right_bottom_point = ordered[max_y_it - 2]
            self.right_top_point = ordered[max_y_it - 3]

    def parallel_to_x(self):
        if self.left_bottom_point[1] != self.right_bottom_point[1]:
            angle_with_x = angle(
                (self.left_bottom_point, self.right_bottom_point),
                ((0, 0), (1, 0))
            )
            if self.left_bottom_point[1] < self.right_bottom_point[1]:
                self.vertices = rotate_around_the_point(
                    self.vertices,
                    self.left_bottom_point,
                    angle_with_x)
            elif self.left_bottom_point[1] > self.right_bottom_point[1]:
                self.vertices = rotate_around_the_point(
                    self.vertices,
                    self.right_bottom_point,
                    -angle_with_x)
            self.order_points()
            self.calc_bounds()

    def shift(self, x, y):
        for it, vert in enumerate(self.vertices):
            self.vertices[it] = (vert[0] + x, vert[1] + y)
        self.calc_bounds()

    def plot(self):
        to_plot = list(self.vertices)
        to_plot.append(to_plot[0])
        figure_x, figure_y = zip(*to_plot)
        plt.plot(figure_x, figure_y, color="orange")

        plt.show()