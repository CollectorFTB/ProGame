import numpy


def gcd(a, b):
    if b > a:
        return gcd(b, a)

    if a % b == 0:
        return b

    return gcd(b, a % b)


def file_path(file_name):
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
    
    :param width: width of picture
    :param height: height of picture
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
    x_collide = image.rx < touch.x < image.rx + image.texture.size[0]
    y_collide = image.ry < touch.y < image.ry + image.texture.size[1]
    return x_collide and y_collide
