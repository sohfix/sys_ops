import os
import sqlite3
from rich import print
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
                                id TEXT PRIMARY KEY,
                                name TEXT NOT NULL,
                                content TEXT NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS todos (
                                id TEXT PRIMARY KEY,
                                content TEXT NOT NULL,
                                deadline TEXT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS hours (
                                id TEXT PRIMARY KEY,
                                job_name TEXT NOT NULL,
                                hours_worked REAL NOT NULL,
                                date TEXT NOT NULL
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS appointments (
                                id TEXT PRIMARY KEY,
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

class HourTracker(DatabaseManager):
    def __init__(self):
        super().__init__()

    def set_total_hours(self, total_hours):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO service_hours (total_hours, remaining_hours) VALUES (?, ?)",
                         (total_hours, total_hours))
        print(f"[green]Total service hours set to {total_hours}.[/green]")

    def log_hours(self, job_name, hours_worked, date=None):
        hour_id = str(uuid.uuid4())
        date = date or datetime.now().strftime("%Y-%m-%d")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO hours (id, job_name, hours_worked, date) VALUES (?, ?, ?, ?)",
                         (hour_id, job_name, hours_worked, date))
            conn.execute("UPDATE service_hours SET remaining_hours = remaining_hours - ? WHERE id = 1",
                         (hours_worked,))
        print(f"[green]Hours logged successfully with ID:[/green] {hour_id}")

    def view_hours(self, date=None):
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT id, job_name, hours_worked, date FROM hours WHERE 1=1"
            params = []
            if date:
                query += " AND date = ?"
                params.append(date)
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def show_remaining_hours(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT remaining_hours FROM service_hours WHERE id = 1")
            result = cursor.fetchone()
            if result:
                remaining_hours = result[0]
                print(f"[green]Remaining service hours: {remaining_hours}[/green]")
            else:
                print("[red]No service hours set yet.[/red]")

class NoteManager(DatabaseManager):
    def __init__(self):
        super().__init__()

    def add_note(self, name, content):
        note_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO notes (id, name, content, timestamp) VALUES (?, ?, ?, ?)",
                         (note_id, name, content, timestamp))
        print(f"[green]Note added successfully with ID:[/green] {note_id}")

    def search_notes(self, keyword):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, name, content, timestamp FROM notes WHERE content LIKE ? OR name LIKE ?",
                                  ('%' + keyword + '%', '%' + keyword + '%'))
            return cursor.fetchall()

    def list_notes(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, name, content, timestamp FROM notes")
            return cursor.fetchall()

    def update_note(self, note_id, new_name=None, new_content=None):
        with sqlite3.connect(self.db_path) as conn:
            if new_name:
                conn.execute("UPDATE notes SET name = ? WHERE id = ?", (new_name, note_id))
            if new_content:
                conn.execute("UPDATE notes SET content = ? WHERE id = ?", (new_content, note_id))
        print(f"[green]Note ID {note_id} updated successfully.[/green]")

    def delete_note(self, note_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        print(f"[green]Note ID {note_id} deleted successfully.[/green]")

    def pretty_print_notes(self, notes):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Name", width=20)
        table.add_column("Content", width=50)
        table.add_column("Timestamp", width=20)

        for note in notes:
            table.add_row(note[0], note[1], note[2], note[3])

        console.print(table)

class ToDoManager(DatabaseManager):
    def __init__(self):
        super().__init__()

    def add_todo(self, content, deadline=None):
        todo_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO todos (id, content, deadline, timestamp) VALUES (?, ?, ?, ?)",
                         (todo_id, content, deadline, timestamp))
        print(f"[green]To-Do added successfully with ID:[/green] {todo_id}")

    def search_todos(self, keyword):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, content, deadline, timestamp FROM todos WHERE content LIKE ?", ('%' + keyword + '%',))
            return cursor.fetchall()

    def list_todos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, content, deadline, timestamp FROM todos")
            return cursor.fetchall()

    def update_todo(self, todo_id, new_content=None, new_deadline=None):
        with sqlite3.connect(self.db_path) as conn:
            if new_content:
                conn.execute("UPDATE todos SET content = ? WHERE id = ?", (new_content, todo_id))
            if new_deadline:
                conn.execute("UPDATE todos SET deadline = ? WHERE id = ?", (new_deadline, todo_id))
        print(f"[green]To-Do ID {todo_id} updated successfully.[/green]")

    def delete_todo(self, todo_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        print(f"[green]To-Do ID {todo_id} deleted successfully.[/green]")

    def pretty_print_todos(self, todos):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Content", width=50)
        table.add_column("Deadline", width=20)
        table.add_column("Timestamp", width=20)

        for todo in todos:
            table.add_row(todo[0], todo[1], todo[2] or "No deadline", todo[3])

        console.print(table)

class CalendarManager(DatabaseManager):
    def __init__(self):
        super().__init__()

    def add_appointment(self, title, date, time=None, description=None):
        appointment_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO appointments (id, title, date, time, description) VALUES (?, ?, ?, ?, ?)",
                         (appointment_id, title, date, time, description))
        print(f"[green]Appointment added successfully with ID:[/green] {appointment_id}")

    def view_appointments(self, date=None):
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT id, title, date, time, description FROM appointments WHERE 1=1"
            params = []
            if date:
                query += " AND date = ?"
                params.append(date)
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def list_appointments(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, title, date, time, description FROM appointments")
            return cursor.fetchall()

    def update_appointment(self, appointment_id, new_title=None, new_date=None, new_time=None, new_description=None):
        with sqlite3.connect(self.db_path) as conn:
            if new_title:
                conn.execute("UPDATE appointments SET title = ? WHERE id = ?", (new_title, appointment_id))
            if new_date:
                conn.execute("UPDATE appointments SET date = ? WHERE id = ?", (new_date, appointment_id))
            if new_time:
                conn.execute("UPDATE appointments SET time = ? WHERE id = ?", (new_time, appointment_id))
            if new_description:
                conn.execute("UPDATE appointments SET description = ? WHERE id = ?", (new_description, appointment_id))
        print(f"[green]Appointment ID {appointment_id} updated successfully.[/green]")

    def delete_appointment(self, appointment_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        print(f"[green]Appointment ID {appointment_id} deleted successfully.[/green]")

    def pretty_print_appointments(self, appointments):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Title", width=20)
        table.add_column("Date", width=15)
        table.add_column("Time", width=10)
        table.add_column("Description", width=40)

        for appointment in appointments:
            table.add_row(appointment[0], appointment[1], appointment[2], appointment[3] or "All Day", appointment[4] or "No description")

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
            table.add_row(*row)

        self.console.print(table)

    def pretty_print(self, title, content):
        """Pretty prints content within a titled panel."""
        panel = Panel(content, title=title, title_align="left", border_style="green")
        self.console.print(panel)

    def format_comparison(self, old_data, new_data, headers):
        """Formats a comparison grid showing old vs new data."""
        table = Table(show_header=True, header_style="bold magenta")
        for header in headers:
            table.add_column(header)

        for old, new in zip(old_data, new_data):
            table.add_row(f"[red]{old}[/red]", f"[green]{new}[/green]")

        self.console.print(table)

    def format_layout(self, panels):
        """Formats a multi-panel layout."""
        layout = Layout()
        for title, content in panels.items():
            panel = Panel(content, title=title, title_align="left", border_style="blue")
            layout.split_column(Layout(panel))

        self.console.print(layout)
