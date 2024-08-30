from .inspector import SQLiteDBInspector
from .managers import ToDoManager, HourTracker, CalendarManager, Formatter, NoteManager

# Initialize instances of each class and store them in a list
all_modules = [NoteManager(), ToDoManager(), HourTracker(), Formatter(), CalendarManager(), SQLiteDBInspector()]
