from kivy.config import Config
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from util import *
from dataStructures import NormImage

import cv2
# from copy import copy
# import random
# import math

WIDTH = 0
HEIGHT = 0


def configure(mode):
    global WIDTH
    global HEIGHT
    if mode == 1:
        Config.set('graphics', 'maximized', 1)
        WIDTH = 1920
        HEIGHT = 1080
    else:
        WIDTH = 1280
        HEIGHT = 720
    Config.set('graphics', 'resizable', 0)
    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'width', str(WIDTH))
    Config.set('graphics', 'height', str(HEIGHT))

    Config.write()


class ProGame(FloatLayout):
    def __init__(self, **kwargs):
        super(ProGame, self).__init__(**kwargs)

        # Request keyboard
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

        # background = create_background(WIDTH, HEIGHT, 1)
        # cv2.imwrite(file_path('white'+str(HEIGHT)+'.png'), background)

        # White background (temporary)
        self.add_image(file_path('white'+str(HEIGHT)+'.png'), 0, 0)
        self.background = self.children[0]

        # Mouse movements
        self.down = False
        self.touch_list = list()

        """
        img = cv2.imread(file_path('white.png'), 1)
        img = make_grid(img, 10)
        cv2.imwrite(file_path('grid.png'), img)
        """

        # X button
        self.add_image(file_path("fileclose.png"), WIDTH-150, HEIGHT-150)
        self.close_button = self.children[0]

        self.last_clicked = None

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        # Window.stop()  #  also works, not sure what the difference is ??
        App.get_running_app().stop()
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.last_clicked = keycode
        print(keycode)
        if keycode[1] == 'd' and list(modifiers).count("ctrl") == 1 and list(modifiers).count("alt") == 1:
            keyboard.release()
        return True

    def add_image(self, source, x, y,  *largs):
        to_add = NormImage(source=source, x=x, y=y)
        to_add.x += to_add.texture.size[0]/2  # corner image instead of center
        to_add.y += to_add.texture.size[1]/2
        to_add.x -= WIDTH/2  # fix FloatLayout inconsistency, normalize to corner of screen
        to_add.y -= HEIGHT/2

        self.add_widget(to_add)

    def on_touch_move(self, touch):
        if self.down:
            Clock.schedule_once(partial(self.add_image, file_path("xd.png"), touch.x, touch.y))

    def on_touch_down(self, touch):
        self.down = True
        if image_collide(touch, self.close_button):
            App.get_running_app().stop()
        # Clock.schedule_once(partial(self.add_image, file_path("xd.png"), touch.x, touch.y))

    def on_touch_up(self, touch):
        self.down = False


class GameApp(App):
    def build(self):
        return ProGame()
