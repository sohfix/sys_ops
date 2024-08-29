# kivy_gui/layouts/baselayout.py
from kivy.uix.boxlayout import BoxLayout

class BaseLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(BaseLayout, self).__init__(**kwargs)
