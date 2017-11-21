import numpy
from dataStructures import NormImage


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


def file_path(file_name):
    """
    finds the file path inside the project directory
    :param file_name: a specific file name (has to be inside the directory Entities
    :return: path inside the main directory to the file specified 
    """
    return "Entities//" + file_name


def make_grid(img, n):
    x = int(0.5+(float(len(img))/n))
    y = x  # int((x*16.0/9.0)+0.5) # uncomment for rectangles
    for i in range(len(img)):
        for j in range(len(img[0])):
            if i % x == 0 or j % y == 0:
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
        if not isinstance(image, NormImage):
            continue
        x_collide = image.rx < touch.x < image.rx + image.texture.size[0]
        y_collide = image.ry < touch.y < image.ry + image.texture.size[1]
        if x_collide and y_collide:
            re.append(image)
    return re
