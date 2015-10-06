import kivy
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', '0')
Config.write()

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ScrollButton(Button):
    pass


class ControlButton(Button):
    pass


class KivyMpd2(App):
    def build(self):
        super(KivyMpd2, self).build()
        container = self.root.ids.container
        for i in range(30):
            container.add_widget(ScrollButton(text=str(i)))
        return self.root


if __name__ == '__main__':
    KivyMpd2().run()