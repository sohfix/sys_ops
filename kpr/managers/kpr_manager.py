import os
import sqlite3
from printy import printy, inputy
from rich.console import Console
from rich.table import Table
from datetime import datetime
import uuid

DB_PATH = os.path.join(os.path.expanduser("~"), "kpr_db", "kpr.db")

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS notes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                uuid TEXT UNIQUE,
                                name TEXT NOT NULL,
                                content TEXT NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS todos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                uuid TEXT UNIQUE,
                                content TEXT NOT NULL,
                                deadline TEXT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS completed_todos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                uuid TEXT UNIQUE,
                                content TEXT NOT NULL,
                                deadline TEXT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                completed_at DATETIME NOT NULL
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS hours (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                uuid TEXT UNIQUE,
                                job_name TEXT NOT NULL,
                                hours_worked REAL NOT NULL,
                                date TEXT NOT NULL
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS appointments (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                uuid TEXT UNIQUE,
                                title TEXT NOT NULL,
                                date TEXT NOT NULL,
                                time TEXT,
                                description TEXT
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS service_hours (
                                id INTEGER PRIMARY KEY,
                                total_hours REAL NOT NULL,
                                remaining_hours REAL NOT NULL
                            )''')

class NoteManager(DatabaseManager):
    def __init__(self):
        super().__init__()

    def add_note(self, name, content):
        note_uuid = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO notes (uuid, name, content, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (note_uuid, name, content, timestamp))
        printy(f"Note added successfully.")

    def search_notes(self, keyword):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT id, name, content, timestamp
                FROM notes
                WHERE name LIKE ? OR content LIKE ?
            ''', ('%' + keyword + '%', '%' + keyword + '%'))
            return cursor.fetchall()

    def update_note_by_index(self, keyword):
        matches = self.search_notes(keyword)
        if matches:
            self.pretty_print_notes(matches)
            index = int(inputy("Select the note by index to update: ", 'c')) - 1
            note_id = matches[index][0]
            new_name = inputy("Enter the new name for the note (optional): ", 'y')
            new_content = inputy("Enter the new content for the note (optional): ", 'y')
            self.update_note_by_id(note_id, new_name, new_content)
        else:
            printy("No matches found.", 'y')

    def update_note_by_id(self, note_id, new_name=None, new_content=None):
        with sqlite3.connect(self.db_path) as conn:
            current_note = self.get_note_by_id(note_id)
            if not current_note:
                printy(f"No note found with ID: {note_id}", 'y')
                return

            new_name = new_name if new_name else current_note[1]
            new_content = new_content if new_content else current_note[2]

            conn.execute('''
                UPDATE notes
                SET name = ?, content = ?, timestamp = ?
                WHERE id = ?
            ''', (new_name, new_content, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), note_id))
        printy(f"Note ID {note_id} updated successfully.", 'c')

    def delete_note_by_index(self, keyword):
        matches = self.search_notes(keyword)
        if matches:
            self.pretty_print_notes(matches)
            index = int(inputy("Select the note by index to delete: ", 'y')) - 1
            note_id = matches[index][0]
            self.delete_note_by_id(note_id)
        else:
            printy("No matches found.", 'Br')

    def delete_note_by_id(self, note_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                DELETE FROM notes WHERE id = ?
            ''', (note_id,))
        printy(f"Note ID {note_id} deleted successfully.", 'c')

    def list_notes(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT id, name, content, timestamp FROM notes
            ''')
            return cursor.fetchall()

    def get_note_by_id(self, note_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT id, name, content, timestamp FROM notes WHERE id = ?
            ''', (note_id,))
            return cursor.fetchone()

    def pretty_print_notes(self, notes):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Name", width=30)
        table.add_column("Content", width=50)
        table.add_column("Timestamp", width=20)

        for note in notes:
            table.add_row(str(note[0]), note[1], note[2], note[3])

        console.print(table)

class ToDoManager(DatabaseManager):
    def __init__(self):
        super().__init__()

    def add_todo(self, content, deadline=None):
        todo_uuid = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO todos (uuid, content, deadline, timestamp) VALUES (?, ?, ?, ?)",
                         (todo_uuid, content, deadline, timestamp))
        printy(f"To-Do added successfully.", 'c')

    def search_todos(self, keyword):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, content, deadline, timestamp FROM todos WHERE content LIKE ?", ('%' + keyword + '%',))
            return cursor.fetchall()

    def list_todos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, content, deadline, timestamp FROM todos")
            return cursor.fetchall()

    def update_todo_by_index(self, keyword):
        matches = self.search_todos(keyword)
        if matches:
            self.pretty_print_todos(matches)
            index = int(inputy("Select the to-do by index to update: ", 'y')) - 1
            todo_id = matches[index][0]
            new_content = inputy("Enter the new content for the to-do: ", 'y')
            new_deadline = input("Enter the new deadline (optional): ", 'y')
            self.update_todo_by_id(todo_id, new_content, new_deadline)
        else:
            printy("No matches found.", 'r')

    def update_todo_by_id(self, todo_id, new_content=None, new_deadline=None):
        with sqlite3.connect(self.db_path) as conn:
            if new_content:
                conn.execute("UPDATE todos SET content = ? WHERE id = ?", (new_content, todo_id))
            if new_deadline:
                conn.execute("UPDATE todos SET deadline = ? WHERE id = ?", (new_deadline, todo_id))
        printy(f"To-Do ID {todo_id} updated successfully.", 'c')

    def delete_todo_by_index(self, keyword):
        matches = self.search_todos(keyword)
        if matches:
            self.pretty_print_todos(matches)
            index = int(inputy("Select the to-do by index to delete: ", 'y')) - 1
            todo_id = matches[index][0]
            self.delete_todo_by_id(todo_id)
        else:
            printy("No matches found.", 'r')

    def delete_todo_by_id(self, todo_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        printy(f"To-Do ID {todo_id} deleted successfully.", 'c')

    def mark_completed_by_index(self, keyword):
        matches = self.search_todos(keyword)
        if matches:
            self.pretty_print_todos(matches)
            index = int(inputy("Select the to-do by ID to mark as completed: ", 'y'))
            todo_id = index
            self.mark_completed_by_id(todo_id)
        else:
            printy("No matches found.", 'r')

    def mark_completed_by_id(self, todo_id):
        with sqlite3.connect(self.db_path) as conn:
            todo = conn.execute("SELECT id, content, deadline, timestamp FROM todos WHERE id = ?", (todo_id,)).fetchone()
            if todo:
                conn.execute("INSERT INTO completed_todos (uuid, content, deadline, timestamp, completed_at) VALUES (?, ?, ?, ?, ?)",
                             (str(uuid.uuid4()), todo[1], todo[2], todo[3], datetime.now().strftime("%m/%d/%Y %H:%M:%S")))
                conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
                printy(f"To-Do ID {todo_id} marked as completed.", 'c')
            else:
                printy(f"To-Do ID {todo_id} not found.", 'r')

    def list_completed_todos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, content, deadline, timestamp, completed_at FROM completed_todos")
            return cursor.fetchall()

    def pretty_print_todos(self, todos):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Content", width=50)
        table.add_column("Deadline", width=20)
        table.add_column("Timestamp", width=20)

        for todo in todos:
            table.add_row(str(todo[0]), todo[1], todo[2] or "No deadline", todo[3])

        console.print(table)

    def pretty_print_completed_todos(self, todos):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Content", width=50)
        table.add_column("Deadline", width=20)
        table.add_column("Created At", width=20)
        table.add_column("Completed At", width=20)

        for todo in todos:
            table.add_row(str(todo[0]), todo[1], todo[2] or "No deadline", todo[3], todo[4])

        console.print(table)

class HourTracker(DatabaseManager):
    def __init__(self):
        super().__init__()

    def set_total_hours(self, total_hours):
        with sqlite3.connect(self.db_path) as conn:
            # Update the service hours if they already exist
            conn.execute("""
                INSERT OR REPLACE INTO service_hours (id, total_hours, remaining_hours)
                VALUES (1, ?, ?)
            """, (total_hours, total_hours))
        printy(f"Total service hours set to {total_hours}.", 'b')

    def log_hours(self, job_name, hours_worked, date=None):
        hour_uuid = str(uuid.uuid4())
        date = date or datetime.now().strftime("%m/%d/%Y")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO hours (uuid, job_name, hours_worked, date) VALUES (?, ?, ?, ?)",
                         (hour_uuid, job_name, hours_worked, date))
            conn.execute("UPDATE service_hours SET remaining_hours = remaining_hours - ? WHERE id = 1",
                         (hours_worked,))
        printy(f"Hours logged successfully.", 'c')

    def view_hours(self, date=None):
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT id, job_name, hours_worked, date FROM hours WHERE 1=1"
            params = []
            if date:
                query += " AND date = ?"
                params.append(date)
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def update_hours_by_index(self, keyword):
        matches = self.view_hours()
        if matches:
            self.pretty_print_hours(matches)
            index = int(input("Select the entry by index to update: ")) - 1
            hour_id = matches[index][0]
            new_hours = float(input("Enter the new hours worked: "))
            new_date = input("Enter the new date (optional): ")
            self.update_hours_by_id(hour_id, new_hours, new_date)
        else:
            printy("No matches found.", 'r')

    def update_hours_by_id(self, hour_id, new_hours, new_date=None):
        with sqlite3.connect(self.db_path) as conn:
            # Get current hours worked
            old_hours = conn.execute("SELECT hours_worked FROM hours WHERE id = ?", (hour_id,)).fetchone()[0]
            conn.execute("UPDATE hours SET hours_worked = ?, date = ? WHERE id = ?",
                         (new_hours, new_date or datetime.now().strftime("%m/%d/%Y"), hour_id))
            conn.execute("UPDATE service_hours SET remaining_hours = remaining_hours + ? - ? WHERE id = 1",
                         (old_hours, new_hours))
        printy(f"Hours ID {hour_id} updated successfully.", 'c')

    def delete_hours_by_index(self, keyword):
        matches = self.view_hours()
        if matches:
            self.pretty_print_hours(matches)
            index = int(inputy("Select the entry by index to delete: ", 'c')) - 1
            hour_id = matches[index][0]
            self.delete_hours_by_id(hour_id)
        else:
            printy("No matches found.", 'r')

    def delete_hours_by_id(self, hour_id):
        with sqlite3.connect(self.db_path) as conn:
            # Get current hours worked before deletion
            old_hours = conn.execute("SELECT hours_worked FROM hours WHERE id = ?", (hour_id,)).fetchone()[0]
            conn.execute("DELETE FROM hours WHERE id = ?", (hour_id,))
            conn.execute("UPDATE service_hours SET remaining_hours = remaining_hours + ? WHERE id = 1",
                         (old_hours,))
        printy(f"Hours ID {hour_id} deleted successfully.", 'c')

    def show_remaining_hours(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT remaining_hours FROM service_hours WHERE id = 1")
            result = cursor.fetchone()
            if result:
                remaining_hours = result[0]
                printy(f"Remaining service hours: {remaining_hours}", 'c')
            else:
                printy("No service hours set yet.", 'y')

    def pretty_print_hours(self, hours):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Job Name", width=30)
        table.add_column("Hours Worked", width=20)
        table.add_column("Date", width=20)

        for hour in hours:
            table.add_row(str(hour[0]), hour[1], str(hour[2]), hour[3])

        console.print(table)

class CalendarManager(DatabaseManager):
    def __init__(self):
        super().__init__()

    def add_appointment(self, title, date, time=None, description=None):
        appointment_uuid = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO appointments (uuid, title, date, time, description) VALUES (?, ?, ?, ?, ?)",
                         (appointment_uuid, title, date, time, description))
        printy(f"Appointment added successfully.", 'c')

    def view_appointments(self, date=None):
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT id, title, date, time, description FROM appointments WHERE 1=1"
            params = []
            if date:
                query += " AND date = ?"
                params.append(date)
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def update_appointment_by_index(self, keyword):
        matches = self.view_appointments()
        if matches:
            self.pretty_print_appointments(matches)
            index = int(input("Select the appointment by index to update: ")) - 1
            appointment_id = matches[index][0]
            new_title = inputy("Enter the new title: ", 'g')
            new_date = inputy("Enter the new date: ", 'g')
            new_time = inputy("Enter the new time: ", 'g')
            new_description = inputy("Enter the new description: ", 'g')
            self.update_appointment_by_id(appointment_id, new_title, new_date, new_time, new_description)
        else:
            printy("No matches found.", 'r')

    def update_appointment_by_id(self, appointment_id, new_title=None, new_date=None, new_time=None, new_description=None):
        with sqlite3.connect(self.db_path) as conn:
            if new_title:
                conn.execute("UPDATE appointments SET title = ? WHERE id = ?", (new_title, appointment_id))
            if new_date:
                conn.execute("UPDATE appointments SET date = ? WHERE id = ?", (new_date, appointment_id))
            if new_time:
                conn.execute("UPDATE appointments SET time = ? WHERE id = ?", (new_time, appointment_id))
            if new_description:
                conn.execute("UPDATE appointments SET description = ? WHERE id = ?", (new_description, appointment_id))
        printy(f"Appointment ID {appointment_id} updated successfully.", 'c')

    def delete_appointment_by_index(self, keyword):
        matches = self.view_appointments()
        if matches:
            self.pretty_print_appointments(matches)
            index = int(input("Select the appointment by index to delete: ")) - 1
            appointment_id = matches[index][0]
            self.delete_appointment_by_id(appointment_id)
        else:
            printy("No matches found.", 'r')

    def delete_appointment_by_id(self, appointment_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        printy(f"Appointment ID {appointment_id} deleted successfully.", 'c')

    def list_appointments(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, title, date, time, description FROM appointments")
            return cursor.fetchall()

    def pretty_print_appointments(self, appointments):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Title", width=30)
        table.add_column("Date", width=20)
        table.add_column("Time", width=15)
        table.add_column("Description", width=40)

        for appointment in appointments:
            table.add_row(str(appointment[0]), appointment[1], appointment[2], appointment[3] or "All Day", appointment[4] or "No description")

        console.print(table)

class Formatter:
    def __init__(self):
        self.console = Console()

    def format_grid(self, data, headers):
        """Formats a grid (table) with the provided data and headers."""
        table = Table(show_header=True, header_style="bold magenta")
        for header in headers:
            table.add_column(header)

        for row in data:
            table.add_row(*[str(cell) for cell in row])

        self.console.print(table)

    def pretty_print(self, title, content):
        """Pretty prints content within a titled panel."""
        panel = Panel(content, title=title, title_align="left", border_style="green")
        self.console.print(panel)

    def format_comparison(self, old_data, new_data, headers):
        """Formats a comparison grid showing old vs new data."""
        table = Table(show_header=True, header_style="bold magenta")
        for header in headers, :
            table.add_column(header)

        for old, new in zip(old_data, new_data):
            table.add_row(f"{old}", f"{new}")

        self.console.print(table)

    def format_layout(self, panels):
        """Formats a multi-panel layout."""
        layout = Layout()
        for title, content in panels.items():
            panel = Panel(content, title=title, title_align="left", border_style="blue")
            layout.split_column(Layout(panel))

        self.console.print(layout)
