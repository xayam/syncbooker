from kivymd.app import MDApp
from kivymd.uix.button import Button


class MyApp(MDApp):
  def build(self):
    return Button(text="Hello World! Привет Мир!")


MyApp().run()
