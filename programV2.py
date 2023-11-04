import argparse
from datetime import datetime
import sqlite3

class TimeManagementApp:
    def __init__(self, db_name="timeManagement.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_records (
            id INTEGER PRIMARY KEY,
            date DATE,
            from_time TEXT,
            to_time TEXT,
            task TEXT,
            tag TEXT
            )
        ''')
        self.conn.commit()

    def record_time(self, user_input_date, from_time, to_time, task, tag):
        today = datetime.now().strftime("%Y/%m/%d") if user_input_date.lower() == "today" else user_input_date

        from_time_parts = from_time.split()
        to_time_parts = to_time.split()

        if len(from_time_parts) == 3:
            from_hours, from_minutes, from_period = from_time_parts
        else:
            from_hours, from_minutes = from_time_parts
            from_period = None

        if len(to_time_parts) == 3:
            to_hours, to_minutes, to_period = to_time_parts
        else:
            to_hours, to_minutes = to_time_parts
            to_period = None

        from_hours = from_hours % 12 + (0 if from_period == "AM" else 12)
        to_hours = to_hours % 12 + (0 if to_period == "AM" else 12)

        from_time_formatted = f"{from_hours:02}:{from_minutes}"
        to_time_formatted = f"{to_hours:02}:{to_minutes}"

        self.cursor.execute("INSERT INTO time_records (date, from_time, to_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                            (today, from_time_formatted, to_time_formatted, task, tag))
        self.conn.commit()
        print("Record submitted successfully")

    def query_records(self, query_request):
        query_request = query_request.strip()

        if query_request.lower() == "all":
            self.cursor.execute("SELECT * FROM time_records")
        elif query_request.lower() == "today":
            today = datetime.now().strftime("%Y/%m/%d")
            self.cursor.execute("SELECT * FROM time_records WHERE date = ?", (today,))
        elif query_request.startswith(":"):
            tag = query_request[1:]
            self.cursor.execute("SELECT * FROM time_records WHERE LOWER(tag) = LOWER(?)", (tag,))
        else:
            if (query_request.startswith("'") and query_request.endswith("'")) or (
                    query_request.startswith('"') and query_request.endswith('"')):
                task = query_request[1:-1]
                self.cursor.execute("SELECT * FROM time_records WHERE task LIKE ?", ('%' + task + '%',))
            else:
                self.cursor.execute("SELECT * FROM time_records WHERE task = ?", (query_request,))

        results = self.cursor.fetchall()

        if results:
            for record in results:
                id, date, from_time, to_time, task, tag = record
                print(f"ID: {id}, Date: {date}, From: {from_time}, To: {to_time}, Task: {task}, Tag: {tag}")
        else:
            print("No records found")

    def run(self):
        while True:
            print("Enter record DATE FROM TO TASK TAG\nOR\nquery query_search (q to quit)")
            user_input = input()

            if user_input.lower() == 'q':
                break

            input_values = user_input.split()

            if len(input_values) >= 5:
                command = input_values[0]
                if command.lower() == "record":
                    user_input_date = input_values[1]
                    from_time = input_values[2]
                    to_time = input_values[3]
                    task_tag_string = ' '.join(input_values[4:])

                    task_parts = task_tag_string.split(':')

                    if len(task_parts) > 1:
                        task = task_parts[0].strip()
                        tag = task_parts[1].strip()
                    else:
                        task = task_parts[0].strip()
                        tag = ""

                    self.record_time(user_input_date, from_time, to_time, task, tag)

                else:
                    print("Invalid command. Try again")

            elif len(input_values) == 2:
                command, query_request = input_values

                if command.lower() == "query":
                    self.query_records(query_request)
                else:
                    print("Command not recognized")

            else:
                print("Invalid input format.")

        self.conn.close()

def main():
    parser = argparse.ArgumentParser(description="Time Management Application")
    parser.add_argument("-r", "--record", nargs="+", help="Record time usage")
    parser.add_argument("-q", "--query", help="Query time usage")

    args = parser.parse_args()
    app = TimeManagementApp()

    if args.record:
        user_input = "record " + " ".join(args.record)
        input_values = user_input.split()
        command = input_values[0]
        if command.lower() == "record":
            user_input_date = input_values[1]
            from_time = input_values[2]
            to_time = input_values[3]
            task_tag_string = ' '.join(input_values[4:])
            task_parts = task_tag_string.split(':')

            if len(task_parts) > 1:
                task = task_parts[0].strip()
                tag = task_parts[1].strip()
            else:
                task = task_parts[0].strip()
                tag = ""

            app.record_time(user_input_date, from_time, to_time, task, tag)

    if args.query:
        query_request = args.query
        app.query_records(query_request)

    app.run()

if __name__ == "__main__":
    main()
