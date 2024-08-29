# kivy_gui/screens/basescreen.py
from kivy.uix.screenmanager import Screen

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
