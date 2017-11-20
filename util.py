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
    print(x, y)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if i % x == 0 or j % y == 0:
                img[i][j] = [0, 0, 0]
    return img


def create_background(height, width, color): # 0 for black, 1 for white
    re = numpy.zeros((width, height, 3), numpy.uint8)
    print(len(re), len(re[0]), len(re[0][0]))
    if color == 1:
        for i in range(height):
            for j in range(width):
                re[j][i] = [255, 255, 255]
    return re


def image_collide(touch, image):
    x_collide = image.rx < touch.x < image.rx + image.texture.size[0]
    y_collide = image.ry < touch.y < image.ry + image.texture.size[1]
    return x_collide and y_collide
