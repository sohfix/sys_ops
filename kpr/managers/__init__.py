from .kpr_manager import NoteManager, ToDoManager, HourTracker, Formatter, CalendarManager
from .logs import Logger
# Initialize instances of each class and store them in a list
all_modules = [NoteManager(), ToDoManager(), HourTracker(), Formatter(), CalendarManager()]
