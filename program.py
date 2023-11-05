from collections import Counter
from datetime import datetime
import sqlite3
import argparse

DATE_FORMAT = "%Y/%m/%d"


class TimeManagementTool:
    def __init__(self, database_file="timeManagement.db"):
        self.database_file = database_file
        self.conn, self.cursor = self._open_database()

    def _open_database(self):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        self._create_table(cursor)
        return conn, cursor

    def _create_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_records (
            id INTEGER PRIMARY KEY,
            date DATE,
            from_time TEXT,
            to_time TEXT,
            task TEXT,
            tag TEXT
            )
        ''')

    def _close_database(self):
        self.conn.close()

    def _record_time(self, date, from_time, to_time, task, tag):
        self.cursor.execute("INSERT INTO time_records (date, from_time, to_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                            (date, from_time, to_time, task, tag))
        self.conn.commit()

    def query_records(self, query_request):
        query_request = query_request.strip()

        if query_request.lower() == "all":
            self.query_all_records()
        elif query_request.lower() == "today":
            today = datetime.now().strftime(DATE_FORMAT)
            self.query_records_by_date(today)
        elif query_request.startswith(":"):
            tag = query_request[1:].strip().lower()
            self.query_records_by_tag(tag)
        else:
            if "/" in query_request:
                self.query_records_by_date(query_request)
            else:
                self.query_records_by_task(query_request)

    def query_all_records(self):
        self.cursor.execute("SELECT * FROM time_records")
        self.print_records(self.cursor.fetchall())

    def query_records_by_date(self, date):
        try:
            datetime.strptime(date, DATE_FORMAT)
        except ValueError:
            print("Invalid date format")
            return
        self.cursor.execute("SELECT * FROM time_records WHERE date = ?", (date,))
        self.print_records(self.cursor.fetchall())

    def query_records_by_tag(self, tag):
        tag = tag.strip().lower()
        self.cursor.execute("SELECT * FROM time_records WHERE LOWER(tag) = ?", (tag,))
        self.print_records(self.cursor.fetchall())

    def query_records_by_task(self, task):
        task = task.strip().strip("'")
        self.cursor.execute("SELECT * FROM time_records WHERE task LIKE ?", ('%' + task + '%',))
        self.print_records(self.cursor.fetchall())

    def record(self, date, from_time, to_time, task, tag):
        if date.lower() == "today":
            date = datetime.now().strftime(DATE_FORMAT)
        else:
            try:
                datetime.strptime(date, DATE_FORMAT)
            except ValueError:
                print("Invalid date format")
                return
        self._record_time(date, from_time, to_time, task, tag)
        print("Record submitted successfully")

    def print_records(self, records):
        if records:
            for record in records:
                id, date, from_time, to_time, task, tag = record
                print(f"ID: {id}, Date: {date}, From: {from_time}, To: {to_time}, Task: {task}, Tag: {tag}")
        else:
            print("No records found")

    def report_generator(self, date_from, date_to):
        if date_from.lower() == "today":
            date_from = datetime.now().strftime(DATE_FORMAT)
        if date_to.lower() == "today":
            date_to = datetime.now().strftime(DATE_FORMAT)
        try:
            datetime.strptime(date_from, DATE_FORMAT)
            datetime.strptime(date_to, DATE_FORMAT)
        except ValueError:
            print("Invalid date format")
            return

        self.cursor.execute("SELECT * FROM time_records WHERE date BETWEEN ? AND ?", (date_from, date_to))
        self.print_records(self.cursor.fetchall())

    def priority(self):
        self.cursor.execute("SELECT task FROM time_records")
        tasks = [record[0] for record in self.cursor.fetchall()]
        task_counts = Counter(tasks)
        most_frequent_task = task_counts.most_common(1)
        if most_frequent_task:
            most_frequent_task = most_frequent_task[0][0]
            self.cursor.execute("SELECT * FROM time_records WHERE task = ?", (most_frequent_task,))
            self.print_records(self.cursor.fetchall())
        else:
            print("No frequent activities")


    def close(self):
        self._close_database()


def main():
    parser = argparse.ArgumentParser(description="Time Management Tool")
    parser.add_argument("--database", default="timeManagement.db", help="Database file")
    args = parser.parse_args()

    tool = TimeManagementTool(database_file=args.database)

    print("""
Welcome to the Time Management Application!

To record time, use the following format:
- record DATE FROM_TIME TO_TIME 'TASK' :TAG

To query your records, you have the following options:
- query all
- query today
- query yyyy/mm/dd
- query :TAG

To print a record of activites, use the following format:
- report yyyy/mm/dd yyyy/mm/dd

Please enter your command: (q to quit)
""")

    while True:
        user_input = input("Enter your command: ")

        if user_input.lower() == 'q':
            tool.close()
            break

        input_values = user_input.split()
        command = input_values[0]

        if command.lower() == "record" and len(input_values) >= 5:
            date = input_values[1]
            from_time = input_values[2]
            to_time = input_values[3]
            task = " ".join(input_values[4:])
            tag = ""

            if ":" in task:
                task, tag = task.split(":", 1)
                task = task.strip()
                tag = tag.strip()

            tool.record(date, from_time, to_time, task, tag)
        elif command.lower() == "query" and len(input_values) == 2:
            tool.query_records(input_values[1])
        elif command.lower() == "report" and len(input_values) == 3:
            tool.report_generator(input_values[1], input_values[2])
        elif command.lower() == "priority":
            tool.priority()
        else:
            print("Invalid command. Try again")


if __name__ == "__main__":
    main()
