# kivy_gui/baseapp.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

class BaseApp(App):
    def __init__(self, **kwargs):
        super(BaseApp, self).__init__(**kwargs)
        self.screen_manager = ScreenManager()

    def add_screen(self, screen):
        self.screen_manager.add_widget(screen)

    def build(self):
        return self.screen_manager
