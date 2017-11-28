from kivy.config import Config
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from util import *
from dataStructures import NormImage
import os.path
import cv2
# import random


def configure():
    Config.set('graphics', 'maximized', 1)
    Config.set('graphics', 'resizable', 0)
    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'width', 1920)
    Config.set('graphics', 'height', 1080)
    Config.write()


class ProGame(FloatLayout):
    def __init__(self, **kwargs):

        super(ProGame, self).__init__(**kwargs)

        # class stuff
        self.last_clicked = None
        self.width = 1920
        self.height = 1080
        self.grid_size = 30
        self.grid_width = 120  # self.width/(self.grid_size*4)
        self.grid_height = 90  # self.height/(self.grid_size*3)

        # Request keyboard
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

        ''' shouldn't happen (when source files are deleted)
        # If background doesnt exist, create it
        if not os.path.exists('Entities/white' + str(self.width) + 'x' + str(self.HEIGHT) + '.png'):
            background = create_background(self.width, self.HEIGHT, 1)
            cv2.imwrite(file_path('white' + str(self.width) + 'x' + str(self.HEIGHT)+'.png'), background)

        # If grid doesnt exist, create it
        if not os.path.exists('Entities/grid' + str(self.width) + 'x' + str(self.HEIGHT) + '.png'):
            img = cv2.imread(file_path('white' + str(self.width) + 'x' + str(self.HEIGHT) + '.png'), 1)
            img = make_grid(img, self.grid_size)
            cv2.imwrite(file_path('grid' + str(self.width) + 'x' + str(self.HEIGHT) + '.png'), img)
        '''

        # White background (temporary)
        self.background = self.normalize_image(file_path('grid' + str(self.width) + 'x' + str(self.height)+'.png'), 0, 0)
        self.add_widget(self.background)

        # X button
        self.close_button = self.normalize_image(file_path("fileclose.png"), self.width-150, self.height-150)
        self.add_widget(self.close_button)

        # xd char
        self.xd = self.normalize_image(file_path("xdpic.png"), 0, 0)
        self.xd_appears = False

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        # Window.stop()  #  also works, not sure what the difference is ??
        self.keyboard = None
        App.get_running_app().stop()

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if list(modifiers).count("ctrl") == 1 and list(modifiers).count("alt") == 1 and keycode[1] == 'd':
            keyboard.release()
        if self.xd_appears:
            if key in ['up', 'down', 'left', 'right']:
                self.move_in_direction(self.xd, key)
        return True

    def normalize_image(self, source, x, y,  *largs):
        to_add = NormImage(source=source, x=x, y=y)
        self.fix_coordinates(to_add)
        return to_add

    def fix_coordinates(self, image):
        image.x = image.rx + (image.texture.size[0] / 2)  # corner image instead of center
        image.y = image.ry + (image.texture.size[1] / 2)
        image.x = image.x - (self.width / 2)  # fix FloatLayout inconsistency, normalize to corner of screen
        image.y = image.y - (self.height / 2)

    def on_touch_down(self, touch):
        if not self.xd_appears:
            self.xd.rx = int(self.grid_width * (touch.x // self.grid_width))
            self.xd.ry = int(self.grid_height * (touch.y // self.grid_height))
            self.fix_coordinates(self.xd)

            self.add_widget(self.xd)
            self.xd_appears = True
        if image_collide(touch, self.close_button):
            App.get_running_app().stop()

    def move_in_direction(self, image, direction):
        if direction is 'right':
            image.rx = (image.rx + self.grid_width) % self.width
        if direction is 'left':
            image.rx = (image.rx - self.grid_width) % self.width
        if direction is 'up':
            image.ry = (image.ry + self.grid_height) % self.height
        if direction is 'down':
            image.ry = (image.ry - self.grid_height) % self.height
        self.fix_coordinates(image)


class GameApp(App):
    def build(self):
        return ProGame()
