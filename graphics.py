from kivy.app import App
from kivy.uix.image import Image
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from util import file_path
from dataStructures import NormImage
# from copy import copy
# import random
# import math

WIDTH = 0
HEIGHT = 0


def configure(mode):
    if mode == 1:
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'borderless', 1)
        Config.set('graphics', 'fullscreen', 'auto')
        #  Window.size = (1920, 1080)
        #  global WIDTH
        #  global HEIGHT
        #  WIDTH = 1920
        #  HEIGHT = 1080
    else:
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'borderless', 0)
        Config.set('graphics', 'fullscreen', 0)
        Window.size = (800, 600)
        global WIDTH
        global HEIGHT
        WIDTH = 800
        HEIGHT = 600
    Config.write()


class ProGame(FloatLayout):
    def __init__(self, **kwargs):
        super(ProGame, self).__init__(**kwargs)

        # Request keyboard
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

        # White background (temporary)
        self.add_image(file_path("white.png"), 0, 0)
        self.background = self.children[0]

        # X button
        self.add_image(file_path("fileclose.png"), 600, 400)
        self.close_button = self.children[0]

        self.last_clicked = None

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        # Window.stop()  #  also works, not sure what the difference is ??
        App.get_running_app().stop()
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.last_clicked = keycode
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

    def on_touch_down(self, touch):
        print(self.close_button.rx, touch.x, self.close_button.rx+self.close_button.texture.size[0])
        if self.close_button.rx < touch.x < self.close_button.rx+self.close_button.texture.size[0] and \
                self.close_button.ry < touch.y < self.close_button.ry+self.close_button.texture.size[1]:
            print('1')
            App.get_running_app().stop()
        x = touch.x
        y = touch.y
        source = file_path("xd.png")
        Clock.schedule_once(partial(self.add_image, source, x, y), 0.2)


class GameApp(App):
    def build(self):
        return ProGame()
