# kivy_gui/utils/theming.py
class Theme:
    PRIMARY_COLOR = [1, 0, 0, 1]  # Example red color in RGBA

    @staticmethod
    def apply_theme(widget):
        widget.color = Theme.PRIMARY_COLOR
