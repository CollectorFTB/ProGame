from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
import random
import math


def configure():
    Config.set('graphics', 'resizable', 0)
    # Window.size = (1600, 900)


class ProGame(FloatLayout):
    def __init__(self, **kwargs):
        super(ProGame, self).__init__(**kwargs)
        self.background = Image(source="C:\Users\gilad\Desktop\october.png")


class GameApp(App):
    def build(self):
        return ProGame()