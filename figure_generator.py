import png
import math
import random as rand


class FigureGenerator:

    def __init__(self, pic_size=100):
        self.__pic_size = pic_size
        self.__fig_size = 0
        self.__fig_size = pic_size - pic_size // 4
        self.__pic = []
        self.__fig = []
        self.__save_path = "../../Desktop/Заборовский/FigureGenerator/"
        self.__generate_pic_background()

    def __generate_pic_background(self):
        self.__pic.clear()
        for i in range(self.__pic_size):
            self.__pic.append([x * 0 + 255 for x in range(self.__pic_size)])

    def __generate_triangle(self):
        self.__fig.clear()
        for i in range(self.__fig_size):
            self.__fig.append([x * 0 + 255 for x in range(self.__fig_size)])
        x1 = self.__fig_size - 1
        y1 = self.__fig_size - 1
        x2 = self.__fig_size - 1
        y2 = 0
        h = round(abs(y2 - y1) * math.sqrt(3)/2)
        self.__x3 = self.__x4 = abs(self.__fig_size - 1 - h)
        y3 = abs(y2 - y1) // 2

        self.__draw_line(x1, y1, x2, y2)
        self.__draw_line(x1, y1,  self.__x3, y3)
        self.__draw_line(self.__x3, y3, x2, y2)
        self.__fill_figure()
        self.__save_pic()

    def __generate_square(self):
        self.__fig.clear()
        for i in range(self.__fig_size):
            self.__fig.append([x * 0 for x in range(self.__fig_size)])
        self.__save_pic()

    def __generate_hexagon(self):
        self.__fig.clear()
        for i in range(self.__fig_size):
            self.__fig.append([x * 0 + 255 for x in range(self.__fig_size)])
        x1 = x4 = cx = cy = self.__fig_size // 2
        y1 = 0
        y4 = self.__fig_size - 1
        h = round(abs(y4 - y1) // 2 * math.sqrt(3) / 2)
        self.__x3 = x2 = x3 = cx - h
        self.__x4 = x5 = x6 = cx + h
        y2 = y6 = cy - abs(y4 - y1) // 4
        y3 = y5 = cy + abs(y4 - y1) // 4
        self.__draw_line(x1, y1, x2, y2)
        self.__draw_line(x3, y3, x2, y2)
        self.__draw_line(x3, y3, x4, y4)
        self.__draw_line(x5, y5, x4, y4)
        self.__draw_line(x5, y5, x6, y6)
        self.__draw_line(x1, y1, x6, y6)
        self.__fill_figure()
        self.__save_pic()

    def __save_pic(self):
        x_shift = rand.choice(range(2, self.__pic_size - self.__fig_size - 2))
        y_shift = rand.choice(range(2, self.__pic_size - self.__fig_size - 2))
        i_fig = j_fig = 0
        for i in range(x_shift, x_shift + self.__fig_size):
            j_fig = 0
            for j in range(y_shift, y_shift + self.__fig_size):
                self.__pic[i][j] = self.__fig[i_fig][j_fig]
                j_fig += 1
            i_fig += 1

        self.__deform_pic()
        png.from_array(self.__pic, 'L').save(self.__save_path + ".png")
        self.__generate_pic_background()

    def __deform_pic(self):
        for i in range(rand.choice(range(2, 10))):
            for i in range(self.__pic_size - 1):
                for j in range(self.__pic_size - 1):
                    square = [[self.__pic[i][j], self.__pic[i][j+1]], [self.__pic[i+1][j], self.__pic[i+1][j+1]]]
                    rev_pix = self.__random_deform_square(square)
                    if rev_pix[0]: self.__reverce_pixel(i, j)
                    if rev_pix[1]: self.__reverce_pixel(i, j+1)
                    if rev_pix[2]: self.__reverce_pixel(i+1, j)
                    if rev_pix[3]: self.__reverce_pixel(i+1, j+1)

    def __reverce_pixel(self, x, y):
        if self.__pic[x][y] == 0:
            self.__pic[x][y] = 255
        else:
            self.__pic[x][y] = 0

    def __random_deform_square(self, square):
        rand20 = rand.choice(range(20)) == 1
        rand10_1 = rand.choice(range(10)) == 1
        rand10_2 = rand.choice(range(10)) == 1
        if square == [[255, 255], [255, 0]]:  # A
            return [rand20, rand10_1, rand10_2, False]
        elif square == [[255, 255], [0, 255]]:  # B
            return [rand10_1, rand20, False, rand10_2]
        elif square == [[0, 0], [255, 255]]:  # C
            return [False, False, rand10_1, rand10_2]
        elif square == [[255, 0], [255, 255]]:  # D
            return [rand10_1, False, rand20, rand10_2]
        elif square == [[255, 255], [0, 0]]:  # E
            return [rand10_1, rand10_2, False, False]
        elif square == [[255, 0], [255, 0]]:  # F
            return [rand10_1, False, rand10_2, False]
        elif square == [[255, 0], [0, 255]]:  # G
            return [rand10_1, False, False, rand10_2]
        elif square == [[255, 0], [0, 0]]:  # H
            return [rand10_1, False, False, False]
        elif square == [[0, 255], [255, 255]]:  # I
            return [False, rand10_2, rand10_1, rand20]
        elif square == [[0, 255], [0, 255]]:  # J
            return [False, rand10_1, rand10_2, False]
        elif square == [[0, 255], [0, 255]]:  # K
            return [False, rand10_1, False, rand10_2]
        elif square == [[255, 0], [255, 255]]:  # L
            return [False, rand10_1, False, False]
        elif square == [[0, 0], [255, 0]]:  # M
            return [False, False, rand10_1, False]
        elif square == [[0, 0], [0, 255]]:  # N
            return [False, False, False, rand10_1]
        else:
            return [False, False, False, False]

    def save_triangle(self, path='./'):
        self.__save_path = path
        self.__generate_triangle()

    def save_square(self, path='./'):
        self.__save_path = path
        self.__generate_square()

    def save_hexagon(self, path='./'):
        self.__save_path = path
        self.__generate_hexagon()

    def __fill_figure(self):
        for i in range(self.__fig_size):
            flag = False
            for j in range(self.__fig_size):
                # TODO условие i !=0 для частного случая, когда вершина треугольника в x3 строке
                if self.__fig[i][j] == 0 and i != self.__x3 and i != self.__x4:  #
                    flag = not flag
                if flag:
                    self.__fig[i][j] = 0

    def __set_pixel(self, x, y):
        self.__fig[x][y] = 0

    def __draw_line(self, x1=0, y1=0, x2=0, y2=0):
        dx = x2 - x1
        dy = y2 - y1

        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

        if dx < 0: dx = -dx
        if dy < 0: dy = -dy

        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x, y = x1, y1

        error, t = el / 2, 0

        self.__set_pixel(x, y)

        while t < el:
            error -= es
            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            self.__set_pixel(x, y)


def generate_triangle(size):
    fg = FigureGenerator(size)
    fg.save_triangle()


def generate_square(size):
    fg = FigureGenerator(size)
    fg.save_square()


def generate_hexagon(size):
    fg = FigureGenerator(size)
    fg.save_hexagon()
