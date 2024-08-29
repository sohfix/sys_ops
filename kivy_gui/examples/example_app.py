# kivy_gui/examples/example_app.py
from kivy_gui import BaseApp
from kivy_gui.screens.basescreen import BaseScreen

class MyApp(BaseApp):
    def build(self):
        screen = BaseScreen(name='main')
        self.add_screen(screen)
        return super(MyApp, self).build()

if __name__ == '__main__':
    MyApp().run()
