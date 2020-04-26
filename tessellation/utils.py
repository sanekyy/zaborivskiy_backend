from __future__ import division
from copy import deepcopy
import math
import matplotlib.pyplot as plt
from scipy import array, cos, sin
from numpy import dot

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])


def segment_intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def line_intersection(line1: tuple, line2: tuple):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return (x, y)


def plot_mutiple_figures(figures: list):
    tmp_fig = deepcopy(figures)
    for figure in tmp_fig:
        figure.append(figure[0])
        figure_x, figure_y = zip(*figure)
        plt.plot(figure_x, figure_y, color="orange")

    plt.show()


def plot_one_figure(figure: list):
    figure.append(figure[0])
    figure_x, figure_y = zip(*figure)
    plt.plot(figure_x, figure_y, color="orange")

    plt.show()


def plot_result(surface_orig: list, figures_orig: list, plot_path: str):
    surface = deepcopy(surface_orig)
    figures = deepcopy(figures_orig)
    surface.append(surface[0])
    surface_x, surface_y = zip(*surface)

    plt.cla()
    plt.plot(surface_x, surface_y, color="red")


    for figure in figures:
        figure.append(figure[0])
        figure_x, figure_y = zip(*figure)
        plt.plot(figure_x, figure_y, color="orange")

    plt.axis('off')
    plt.savefig(plot_path, bbox_inches='tight')


def point_around_point(xy, origin, radians, precision):
    """Rotate a point around a given point.

    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    x, y = xy
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    return round(qx, precision), round(qy, precision)


def rotate_around_the_point(pts_list, center, ang, precision=1):
    return [point_around_point(pt, center, ang, precision) for pt in pts_list]


def angle(segm1, segm2):
    vector1 = ((segm1[0][0]-segm1[1][0]), (segm1[0][1]-segm1[1][1]))
    vector2 = ((segm2[0][0]-segm2[1][0]), (segm2[0][1]-segm2[1][1]))
    x1, y1 = vector1
    x2, y2 = vector2
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return round(math.acos(inner_product/(len1*len2)), 2)


def get_len(pt1, pt2):
    return math.sqrt(
            math.pow((pt2[0] - pt1[0]), 2) +
            math.pow((pt2[1] - pt1[1]), 2)
        )


def calc_area(vertices):
        n = len(vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i][0] * vertices[j][1]
            area -= vertices[j][0] * vertices[i][1]
        return abs(area) / 2.0
