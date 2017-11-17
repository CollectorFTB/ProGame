from kivy.app import App
from kivy.uix.button import Button


class TestApp(App):
    def build(self):
        return Button(text='Hello World')


def main():
    TestApp().run()


if __name__ == "__main__":
    main()
