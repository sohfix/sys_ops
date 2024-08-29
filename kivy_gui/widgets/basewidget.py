# kivy_gui/widgets/basewidget.py
from kivy.uix.widget import Widget

class BaseWidget(Widget):
    def __init__(self, **kwargs):
        super(BaseWidget, self).__init__(**kwargs)
