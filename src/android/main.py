from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel


class Container(TabbedPanel):
    pass


class MainApp(App):
    def build(self):
        return Container()


MainApp().run()
