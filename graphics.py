from kivy.config import Config
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from util import *
from dataStructures import NormImage, Animation
from copy import copy
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

        # White background (temporary)
        self.background = self.normalize_image(file_path('grid' + str(self.width) + 'x' + str(self.height)+'.png'), 0, 0)
        self.add_widget(self.background)

        # X button
        self.close_button = self.normalize_image(file_path("fileclose.png"), 14, 10, 1)
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

    def normalize_image(self, source, x, y, *args):  # image factory
        if len(args) > 0:
            x, y = indexes_to_coordinates(y % 12, x % 16, self.grid_width, self.grid_height)
        to_add = NormImage(source=source, x=x, y=y)
        self.fix_coordinates(to_add)
        return to_add

    def fix_coordinates(self, image):
        image.x = image.rx + image.texture.size[0] / 2  # corner image instead of center
        image.y = image.ry + image.texture.size[1] / 2
        image.x = image.x - self.width / 2  # fix FloatLayout inconsistency, normalize to corner of screen
        image.y = image.y - self.height / 2
        image.i = int(self.grid_height * (image.y // self.grid_height))
        image.j = int(self.grid_width * (image.x // self.grid_width))

    def on_touch_down(self, touch):
        if not self.xd_appears:
            self.xd.rx = int(self.grid_width * (touch.x // self.grid_width))
            self.xd.ry = int(self.grid_height * (touch.y // self.grid_height))
            self.fix_coordinates(self.xd)
            self.add_widget(self.xd)
            self.xd_appears = True
        a = copy(self.xd)
        self.add_widget(a)
        self.play_animation(a, circle_points((touch.x, touch.y), 90, 2), 0.05)

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

    def add_event(self, animation, dt):
        animation.next_frame(self.fix_coordinates)

    def play_animation(self, picture, points, refresh_rate):
        Clock.schedule_interval(partial(self.add_event, Animation(points, picture)), refresh_rate)


class GameApp(App):
    def build(self):
        return ProGame()





