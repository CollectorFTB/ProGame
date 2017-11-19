from kivy.app import App
from kivy.uix.image import Image
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from functools import partial
import random
import math


def configure(mode):
    if mode == 1:
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'borderless', 1)
        Config.set('graphics', 'fullscreen', 'auto')
        #  Window.size = (1920, 1080)
    else:
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'borderless', 0)
        Config.set('graphics', 'fullscreen', 0)
        Window.size = (800, 600)
    Config.write()


class ProGame(FloatLayout):
    def __init__(self, **kwargs):
        super(ProGame, self).__init__(**kwargs)
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        self.background = Image(x=0, y=0, source="Entities\\xd.png")
        self.last_clicked = None

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        # Window.stop()  #  also works, not sure what the difference is ??
        App.get_running_app().stop()
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)

        if keycode[1] == 'escape' and list(modifiers).count("ctrl") == 1:
            keyboard.release()

        return True

    def my_callback(self, image, *largs):
        self.add_widget(image)

    def on_touch_down(self, touch):
        if touch.x < 100:
            Clock.schedule_once(partial(self.my_callback, self.background), 2)
        print(touch.x, touch.y)


class GameApp(App):
    def build(self):
        return ProGame()
