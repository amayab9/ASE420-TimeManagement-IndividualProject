#this version turned into a mess when looking for am and pm, so I dropped this file. V2-2 is the working one
#
import argparse
from datetime import datetime
import sqlite3

welcome_prompt = """
Welcome to the Time Management Application!

To record time, use the following format:
record DATE FROM_TIME TO_TIME TASK TAG

To query your records, you have the following options:
- query all
- query today
- query yyyy/mm/dd
- query :TAG

Please enter your command: (q to quit)
"""

class TimeManagementApp:
    def __init(self, db_name="timeManagement.db"):
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

        self.cursor.execute("INSERT INTO time_records (date, from_time, to_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                            (today, from_time, to_time, task, tag))
        self.conn.commit()
        print("Record submitted successfully")

    def query_records(self, query_request):
        query_request = query_request.strip()

        if query_request.lower() == "all":
            self.query_all_records()
        elif query_request.lower() == "today":
            today = datetime.now().strftime("%Y/%m/%d")
            self.query_records_by_date(today)
        elif query_request.startswith(":"):
            tag = query_request[1:]
            self.query_records_by_tag(tag)
        else:
            self.query_records_by_task(query_request)

    def query_all_records(self):
        self.cursor.execute("SELECT * FROM time_records")
        self.print_records(self.cursor.fetchall())

    def query_records_by_date(self, date):
        self.cursor.execute("SELECT * FROM time_records WHERE date = ?", (date,))
        self.print_records(self.cursor.fetchall())

    def query_records_by_tag(self, tag):
        self.cursor.execute("SELECT * FROM time_records WHERE LOWER(tag) = LOWER(?)", (tag,))
        self.print_records(self.cursor.fetchall())

    def query_records_by_task(self, task):
        self.cursor.execute("SELECT * FROM time_records WHERE task LIKE ?", ('%' + task + '%',))
        self.print_records(self.cursor.fetchall())

    def print_records(self, records):
        if records:
            for record in records:
                id, date, from_time, to_time, task, tag = record
                print(f"ID: {id}, Date: {date}, From: {from_time}, To: {to_time}, Task: {task}, Tag: {tag}")
        else:
            print("No records found")

    def run(self):
        print(welcome_prompt)
        while True:
            user_input = input("Please enter your command: ")
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
