import cv2
import numpy as np
import imageio


# import scipy.ndimage
# import os

# types:
# 0 - hexagon
# 1 - square
# 2 -triangle

# def center_image(filename):
#     img = imageio.imread(filename)
#     img = (img - np.min(img)) / (np.max(img) - np.min(img))
#     img = 1 - img
#
#     center_of_image = [coord // 2 for coord in img.shape]
#     midpoint_of_an_object = np.median(np.argwhere(img == 1), axis=0)
#     int_midpoint = [int(coord) for coord in midpoint_of_an_object]
#
#     shift = [i1 - i2 for i1, i2 in zip(center_of_image, int_midpoint)]
#     new_img = scipy.ndimage.shift(img, shift)
#     new_img = 1 - new_img
#     imageio.imwrite('temp', img)


def approximate(filename, class_type, output_filename=None):
    # center_image(filename)
    figure = []
    img = cv2.imread(filename)
    # os.remove('temp')

    if class_type == 0:
        blur = cv2.GaussianBlur(img, (25, 25), 0)
    elif class_type == 1:
        blur = cv2.GaussianBlur(img, (15, 15), 0)
    elif class_type == 2:
        blur = cv2.GaussianBlur(img, (21, 21), 0)
    else:
        return figure

    color = (0, 255, 0)
    thickness = 2
    values = [30, 40, 50, 60, 70, 80, 90, 100]
    # values = [30]
    gray_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    all_contours = []
    for i in values:
        ret, threshold = cv2.threshold(gray_image, i, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area = sorted(contours, key=cv2.contourArea, reverse=True)
        for j in range(1, len(area)):
            contour = area[j]
            # size = cv2.contourArea(contour)
            all_contours.append(contour)
            # cv2.drawContours(img, [contour], -1, (0, 0, 255), 2)
            # if 10 < float(size) < 8000:
            #     cv2.drawContours(img, [contour], -1, (0,255,0), 2)
            #     all_contours.append(contour)

    contour = np.array([], dtype=int)
    for cont in all_contours:
        contour = np.append(contour, cont)
    contour = np.reshape(contour, (-1, 1, 2))
    if contour.size == 0:
        contour = np.array([[[0, 0]], [[100, 100]]], dtype=int)

    x, y, horizontal, vertical = cv2.boundingRect(contour)
    h = (horizontal + vertical) / 2

    if class_type == 2:
        # enclose = cv2.minEnclosingTriangle(contour)
        # figure = np.array([[int(i) for i in enclose[1][j][0]] for j in range(0,3)])
        # cv2.drawContours(img, [figure], -1, color, thickness)
        figure = np.array(
            [[x, y + vertical], [x + horizontal / 2, y], [x + horizontal, y + vertical]], np.int32)

    elif class_type == 1:
        figure = np.array(
            [[x, y], [x + h, y], [x + h, y + h], [x, y + h]], np.int32)

    elif class_type == 0:
        r = h / 2
        figure = np.array(
            [[x + r * 0.5, y], [x + r * 1.5, y], [x + r * 2, y + r], [x + r * 1.5, y + r * 2], [x + r * 0.5, y + 2 * r],
             [x, y + r]], np.int32)
        # figure = figure.reshape((-1, 1, 2))

    # cv2.imshow('img', img)
    if output_filename is not None:
        cv2.polylines(img, [figure], True, color, thickness)
        cv2.imwrite(output_filename, img)

    result = []
    result.append(figure)
    result.append(cv2.contourArea(contour))
    result.append(cv2.arcLength(contour, True))

    return result  # 1 - figure coords 2 - figure area  3 - figure perimetr
