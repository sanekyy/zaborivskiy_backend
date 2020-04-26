from copy import deepcopy
import matplotlib.path as mpl_path
from numpy import pi, arange

from tessellation.figure import Figure
from tessellation.utils import segment_intersect, rotate_around_the_point, \
                            get_len, calc_area, angle, plot_one_figure, plot_result


DIST_BETWEEN = 0.1
ROT_CNT = 16

def max_tessellate(work_surface: Figure, grid: list) \
    -> (list, int, float):
    result_figures: list
    n_figures: int
    area_prop = float("-inf")

    work_surface_area = calc_area(work_surface.vertices)

    center = (
        (work_surface.bounds['left'] + work_surface.bounds['right']) / 2,
        (work_surface.bounds['bottom'] + work_surface.bounds['top']) / 2,
    )

    for ang in arange(0, 2*pi,pi/ROT_CNT):
        rotated_figures = []
        for figure in grid:
            rotated_figures.append(
                rotate_around_the_point(figure, center, ang, 4)
            )
        figure_area = calc_area(rotated_figures[0])
        rotated_trim = polygon_contains(work_surface, rotated_figures)
        rotated_n_figures = len(rotated_trim)
        rotated_area_prop = figure_area * rotated_n_figures / work_surface_area
        if rotated_area_prop > area_prop:
            result_figures = rotated_trim
            n_figures = rotated_n_figures
            area_prop = rotated_area_prop

    return result_figures, n_figures, area_prop


def parallelogram_grid(work_surface: Figure, orig_figure: Figure):
    work_surface.calc_bounds()

    figure = deepcopy(orig_figure)
    figure.order_points()
    figure.calc_bounds()
    figure.parallel_to_x()


    diag_length = get_len(
        (work_surface.bounds['left'], work_surface.bounds['bottom']),
        (work_surface.bounds['right'], work_surface.bounds['top'])
    )
    width = work_surface.bounds['right'] - work_surface.bounds['left']
    height = work_surface.bounds['top'] - work_surface.bounds['bottom']
    width_diff = diag_length - width
    height_diff = diag_length - height

    grid_bounds = {
        "left": work_surface.bounds['left'] - width_diff / 2,
        "right": work_surface.bounds['right'] + width_diff / 2,
        "top": work_surface.bounds['top'] + height_diff / 2,
        "bottom": work_surface.bounds['bottom'] - height_diff / 2
    }

    move_x = figure.right_bottom_point[0] - figure.left_bottom_point[0] + DIST_BETWEEN
    move_y = figure.left_top_point[1] - figure.left_bottom_point[1] + DIST_BETWEEN
    x_shift = grid_bounds['left'] - figure.left_bottom_point[0] - move_x
    y_shift = grid_bounds['top'] - figure.left_bottom_point[1]

    figure.shift(x_shift, y_shift)

    init_step_x = figure.bounds['left']
    current_step_y = figure.bounds['top']
    stop_factor_x = grid_bounds['right'] + move_x
    stop_factor_y = grid_bounds['bottom'] - move_y
    row = 0
    result_figures = []
    while current_step_y > stop_factor_y:
        current_step_x = init_step_x
        column = 0
        while current_step_x < stop_factor_x:
            tile = []
            for vert in figure.vertices:
                tile.append(
                    (vert[0] + column * move_x,
                     vert[1] - row * move_y)
                )
            column += 1
            current_step_x += move_x
            result_figures.append(tile)
        row += 1
        current_step_y -= move_y

    return result_figures


def polygon_contains(work_surface, figures):
    mpl_surface = mpl_path.Path(work_surface.vertices)
    figure_n_vert = len(figures[0]) - 1
    trim_result = []
    for result_figure in figures:
        if all(mpl_surface.contains_points(result_figure)):
            intersect = False
            it_poly = len(work_surface.vertices) - 1
            while it_poly > -1 and not intersect:
                it_figure = figure_n_vert
                while it_figure > -1:
                    intersect = segment_intersect(
                        work_surface.vertices[it_poly], work_surface.vertices[it_poly - 1],
                        result_figure[it_figure], result_figure[it_figure - 1]
                    )
                    it_figure -=1
                it_poly -= 1
            if not intersect:
                trim_result.append(result_figure)

    return trim_result


def parallelogram_tessellation(work_surface: Figure, figure: Figure):
    grid = parallelogram_grid(work_surface, figure)
    return max_tessellate(work_surface, grid)


def triangle_tessellation(work_surface: Figure, figure: Figure):
    result_figures: list
    n_figures: int
    area_prop = float("-inf")

    for it in range(2, -1, -1):
        parallelogram = figure.vertices.copy()
        parallelogram.append(
            (
                parallelogram[it][0] +
                    (parallelogram[it - 1][0] - parallelogram[it - 2][0]),
                parallelogram[it][1] +
                    (parallelogram[it - 1][1] - parallelogram[it - 2][1])
            )
        )

        parallelogram_figure = Figure(parallelogram)

        triangle_sorted_idx = parallelogram_figure.vertices.index(parallelogram[it])

        init_ang = angle(
            (parallelogram_figure.vertices[triangle_sorted_idx],
                parallelogram_figure.vertices[triangle_sorted_idx - 1]),
            (parallelogram_figure.vertices[triangle_sorted_idx],
                parallelogram_figure.vertices[triangle_sorted_idx - 3])
        )

        par_grid = parallelogram_grid(work_surface, parallelogram_figure)

        grid = []

        triangle_init_idx: int
        for it, _ in enumerate(par_grid[0]):
            par_angle = angle(
                (par_grid[0][it], par_grid[0][it - 1]),
                (par_grid[0][it], par_grid[0][it - 3])
            )
            if init_ang == par_angle:
                triangle_init_idx = it
                break

        for grid_figure in par_grid:
            grid.append([
                grid_figure[triangle_init_idx],
                grid_figure[triangle_init_idx - 1],
                grid_figure[triangle_init_idx - 2]
            ])
            grid.append([
                grid_figure[triangle_init_idx],
                grid_figure[triangle_init_idx - 2],
                grid_figure[triangle_init_idx - 3]
            ])

        triangle_loop_fig, triangle_loop_n, triangle_loop_prop = \
            max_tessellate(work_surface, grid)

        if triangle_loop_prop > area_prop:
            result_figures = triangle_loop_fig
            n_figures = triangle_loop_n
            area_prop = triangle_loop_prop


    return result_figures, n_figures, area_prop


def hex_grid(work_surface: Figure, orig_figure: Figure):
    work_surface.calc_bounds()

    figure = deepcopy(orig_figure)
    figure.calc_bounds()

    bottom = float("inf")
    top = float("-inf")
    bottom_vert_idx: int
    top_vert_idx: int
    for it, vert in enumerate(figure.vertices):
        if vert[1] < bottom:
            bottom = vert[1]
            bottom_vert_idx = it
        elif vert[1] == bottom:
            if vert[0] < figure.vertices[bottom_vert_idx][0]:
                bottom = vert[1]
                bottom_vert_idx = it
        if vert[1] > top:
            top = vert[1]
            top_vert_idx = it
        elif vert[1] == top:
            if vert[0] < figure.vertices[top_vert_idx][0]:
                top = vert[1]
                top_vert_idx = it

    if figure.vertices[top_vert_idx][0] < \
        figure.vertices[bottom_vert_idx][0]:
        bottom_vert_idx -= 5
    elif figure.vertices[top_vert_idx][0] > \
        figure.vertices[bottom_vert_idx][0]:
        top_vert_idx -= 1

    diag_x_angle = angle(
        (figure.vertices[bottom_vert_idx], figure.vertices[top_vert_idx]),
        ((0, 0), (1, 0))
    )

    if figure.vertices[bottom_vert_idx][0] != \
        figure.vertices[top_vert_idx][0]:
        figure.vertices = rotate_around_the_point(
            figure.vertices,
            figure.vertices[bottom_vert_idx],
            diag_x_angle - pi / 2
        )

    diag_length = get_len(
        (work_surface.bounds['left'], work_surface.bounds['bottom']),
        (work_surface.bounds['right'], work_surface.bounds['top'])
    )
    width = work_surface.bounds['right'] - work_surface.bounds['left']
    height = work_surface.bounds['top'] - work_surface.bounds['bottom']
    width_diff = diag_length - width
    height_diff = diag_length - height

    grid_bounds = {
        "left": work_surface.bounds['left'] - width_diff / 2,
        "right": work_surface.bounds['right'] + width_diff / 2,
        "top": work_surface.bounds['top'] + height_diff / 2,
        "bottom": work_surface.bounds['bottom'] - height_diff / 2
    }

    figure.calc_bounds()
    width = figure.bounds['right'] - figure.bounds['left']
    move_x = width + DIST_BETWEEN
    move_y = figure.vertices[top_vert_idx][1] - \
        figure.vertices[top_vert_idx - 2][1] + DIST_BETWEEN

    x_shift = grid_bounds['left'] - figure.vertices[bottom_vert_idx][0] - move_x
    y_shift = grid_bounds['top'] - figure.vertices[bottom_vert_idx][1]
    figure.shift(x_shift, y_shift)
    even_figure = deepcopy(figure)
    even_figure.shift(-width / 2, 0)

    init_step_x = figure.bounds['left']
    current_step_y = figure.bounds['top']
    stop_factor_x = grid_bounds['right'] + move_x
    stop_factor_y = grid_bounds['bottom'] - move_y
    row = 0
    result_figures = []
    while current_step_y > stop_factor_y:
        if row % 2 == 0:
            current_step_x = init_step_x - width / 2
            shift_figure = even_figure
        else:
            current_step_x = init_step_x
            shift_figure = figure
        column = 0
        while current_step_x < stop_factor_x:
            tile = []
            for vert in shift_figure.vertices:
                tile.append(
                    (vert[0] + column * move_x,
                     vert[1] - row * move_y)
                )
            column += 1
            current_step_x += move_x
            result_figures.append(tile)
        row += 1
        current_step_y -= move_y

    return result_figures


def hex_tessellation(work_surface: Figure, figure: Figure):
    grid = hex_grid(work_surface, figure)
    return max_tessellate(work_surface, grid)


def tessellation(
    surface_vertices: list,
    figure_vertices: list,
    plot_path:str=None):

    tessellation_func: function
    if len(figure_vertices) == 3:
        tessellation_func = triangle_tessellation
    elif len(figure_vertices) == 4:
        tessellation_func = parallelogram_tessellation
    elif len(figure_vertices) == 6:
        tessellation_func = hex_tessellation
    else:
        raise AssertionError("Figure should be one of - triangle, parallelogram, hexogram")

    work_surface = Figure(surface_vertices)
    figure = Figure(figure_vertices)
    result_figures, n_figures, area_prop = tessellation_func(work_surface, figure)

    if plot_path:
        plot_result(work_surface.vertices, result_figures, plot_path)

    return result_figures, n_figures, area_prop
