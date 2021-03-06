import dataStructures
import numpy
import math
import os


def gcd(a, b):
    """
    gcd(54,24)=6
    gcd(7,15)=1
    gcd(4,8)=4  
    :param a: integer 
    :param b: integer
    :return: returns the greatest common divisor of a and b
    """
    if b > a:
        return gcd(b, a)

    if a % b == 0:
        return b

    return gcd(b, a % b)


def path(file_name, directory):
    """
    finds the file path inside the project directory
    :param file_name: a specific file name (has to be inside the directory specified)
    :param directory: a specific directory
    :return: path inside the main directory to the file specified 
    """
    return os.path.join(directory, file_name)


def make_grid(img, n):
    """
    draw a grid on a given image every n pixels
    :param img: picture to draw on 
    :param n: grid size 
    :return: image with grid drawn on it in place
    """
    x = 4*n
    y = 3*n  # (len(img)//(n*9))*16

    for i in range(len(img)):
        for j in range(len(img[0])):
            if i % y == 0 or j % x == 0:
                img[i][j] = [0, 0, 0]
    return img


def create_background(width, height, color):
    """
    makes a uniform picture in certain color
    :param width: width of desired picture
    :param height: height of desired picture
    :param color: 0=black, 1=white, 2=transparent
    :return: numpy array of an image in requested color
    """
    re = numpy.zeros((height, width, 4), numpy.uint8)
    t = 255  # by default we want a white colored background
    if color >= 1:
        if color == 2:
            t = 0  # alpha channel equals 0 for transparent instead of white
        for i in range(height):
            for j in range(width):
                re[i][j] = [255, 255, 255, t]
    return re


def image_collide(touch, image):
    """
    checks if the touch object collides with the image given
    :param touch: certain click
    :param image: specific image
    :return: whether or not the image
    """
    x_collide = image.rx < touch.x < image.rx + image.texture.size[0]
    y_collide = image.ry < touch.y < image.ry + image.texture.size[1]
    return x_collide and y_collide


def all_image_collide(touch, children):
    """
    checks if the touch object collides with the image given
    :param touch: certain click
    :param children: list of images
    :return: all the images in children that collide with touch
    """
    re = list()
    for image in children:
        if isinstance(image, dataStructures.NormImage):
            if image_collide(touch, image):
                re.append(image)
    return re


def print_points(*points):
    """
    
    :param points: collection of pairs
    :return: None
    """
    to_print = str()
    for point in points:
        to_print += '(' + str(point[0]) + ', ' + str(point[1]) + ')' + '  ####  '
    print(to_print[:-6])  # without ####


def round_digits(number, digits):
    """
    rounds a number do n decimal places
    :param number: number to round
    :param digits: number of digits
    :return: number rounded to digits decimal places
    """
    exponent = pow(10, digits)
    result = int(number * exponent)
    return result / exponent


def circle_points(center, radius, n, direction):
    """
    get list of n points around center with radius r 
    :param center: center of the circle
    :param radius: radius of the circle
    :param n: number of sides for the perfect polygon
    :param direction: clockwise or counter-clockwise
    :return: list of vertices of the polygon
    """
    points = list()
    const = 0
    for i in range(n):
        x = center[0] + radius * math.cos((i * 2 * (math.pi / n)) + const)
        y = center[1] + radius * math.sin((i * 2 * (math.pi / n)) + const)
        x, y = round_digits(x, 4), round_digits(y, 4)
        points.append((int(x), int(y)))
    if direction == 1:  # clockwise
        return points
    elif direction == 0:  # counter clockwise
        return points[-1::-1]
    else:
        return None


def indexes_to_coordinates(i, j, col_size, row_size):
    """
    unit conversion
    :param i: given row 
    :param j: given col
    :param col_size: size of each col
    :param row_size: size of each row
    :return: x,y simulation of given i,j
    """
    x = j * col_size
    y = i * row_size
    return x, y
