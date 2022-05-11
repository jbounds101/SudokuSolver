import numpy as np
import cv2



def array_from_path(path):
    img = cv2.imread(path)
    width_img = height_img = 450

    # Prepare image
    img = cv2.resize(img, (width_img, height_img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale
    img = cv2.GaussianBlur(img, (5, 5), 1)  # Blur
    img = cv2.adaptiveThreshold(img, 255, 1, 1, 11, 2)  # Adaptive threshold, (convert to
    # binary)

    # Get contours
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the biggest contour (find the sudoku board outline)
    largest = np.array([])
    maximum_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            perimeter = cv2.arcLength(i, True)
            approximation = cv2.approxPolyDP(i, 0.02 * perimeter, True)  # check for number of sides
            if area > maximum_area and len(approximation) == 4:  # find squares
                largest = approximation
                maximum_area = area
    if largest.size != 0:
        largest = reorder_points(largest)
        points_one = np.float32(largest)  # Prepare for warp
        points_two = np.float32([[0, 0], [width_img, 0], [0, height_img], [width_img, height_img]])
        matrix = cv2.getPerspectiveTransform(points_one, points_two)
        img = cv2.warpPerspective(img, matrix, (width_img, height_img))


    # Split into each grid cell, and predict the number

    cell_size = width_img / 9
    for row in range(9):
        for column in range(9):
            # TODO This is broken, fix later
            sub_img = img[(cell_size * column):(cell_size * (column + 1)), (cell_size * row):(cell_size * (row + 1))]
            cv2.imshow('sub', sub_img)
            cv2.waitKey(0)

def reorder_points(points):
    points = points.reshape((4, 2))
    points_new = np.zeros((4, 1, 2), dtype='int32')
    add = points.sum(1)
    points_new[0] = points[np.argmin(add)]
    points_new[3] = points[np.argmax(add)]
    difference = np.diff(points, axis=1)
    points_new[1] = points[np.argmin(difference)]
    points_new[2] = points[np.argmax(difference)]
    return points_new
