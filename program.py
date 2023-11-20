from abc import ABC, abstractmethod
from collections import Counter
from datetime import datetime
import sqlite3
import argparse


class Command(ABC):
    @abstractmethod
    def execute(self, tool, input_values):
        pass


class RecordCommand(Command):
    def execute(self, tool, input_values):
        date = input_values[0]
        from_time = input_values[1]
        to_time = input_values[2]
        task = " ".join(input_values[3:])
        tag = ""

        if ":" in task:
            task, tag = task.split(":", 1)
            task = task.strip()
            tag = tag.strip()

        tool.record(date, from_time, to_time, task, tag)


class QueryCommand(Command):
    def execute(self, tool, input_values):
        tool.query_records(input_values[0])


class ReportCommand(Command):
    def execute(self, tool, input_values):
        tool.report_generator(input_values[0], input_values[1])


class PriorityCommand(Command):
    def execute(self, tool, input_values):
        tool.priority()


class Database:
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

    def execute_query(self, query, parameters=None):
        if parameters is None:
            parameters = ()
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def execute_insert(self, query, parameters):
        self.cursor.execute(query, parameters)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def close(self):
        self._close_database()


def print_records(records):
    if records:
        for record in records:
            item_id, date, from_time, to_time, task, tag = record
            print(f"ID: {item_id}, Date: {date}, From: {from_time}, To: {to_time}, Task: {task}, Tag: {tag}")
    else:
        print("No records found")


class TimeManagementTool:
    DATE_FORMAT = "%Y/%m/%d"

    def __init__(self, database):
        self.database = database
        self.conn = self.database.get_connection()
        self.cursor = self.database.get_cursor()

    def process_command(self, command, command_input_values):
        command.execute(self, command_input_values)

    def record(self, date, from_time, to_time, task, tag):
        if date.lower() == "today":
            date = datetime.now().strftime(self.DATE_FORMAT)
        else:
            try:
                datetime.strptime(date, self.DATE_FORMAT)
            except ValueError:
                print("Invalid date format")
                return

        query = "INSERT INTO time_records (date, from_time, to_time, task, tag) VALUES (?, ?, ?, ?, ?)"
        parameters = (date, from_time, to_time, task, tag)
        self.database.execute_insert(query, parameters)
        print("Record submitted successfully")

    def query_records(self, query_request):
        query_request = query_request.strip()

        if query_request.lower() == "today":
            today = datetime.now().strftime(self.DATE_FORMAT)
            self.query_records_by_date(today)
        elif query_request.startswith(":"):
            tag = query_request[1:].strip().lower()
            self.query_records_by_tag(tag)
        else:
            if "/" in query_request:
                self.query_records_by_date(query_request)
            else:
                self.query_records_by_task(query_request)

    def query_records_by_date(self, date):
        if date.lower() == "today":
            date = datetime.now().strftime(self.DATE_FORMAT)
        try:
            datetime.strptime(date, self.DATE_FORMAT)
        except ValueError:
            print("Invalid date format")
            return
        self.cursor.execute("SELECT * FROM time_records WHERE date = ?", (date,))
        print_records(self.cursor.fetchall())

    def query_records_by_tag(self, tag):
        tag = tag.strip().lower()
        query = "SELECT * FROM time_records WHERE LOWER(tag) = ?"
        parameters = (tag,)
        records = self.database.execute_query(query, parameters)
        print_records(records)

    def query_records_by_task(self, task):
        task = task.strip().strip("'")
        query = "SELECT * FROM time_records WHERE task LIKE ?"
        parameters = ('%' + task + '%',)
        records = self.database.execute_query(query, parameters)
        print_records(records)

    def report_generator(self, date_from, date_to):
        if date_from.lower() == "today":
            date_from = datetime.now().strftime(self.DATE_FORMAT)
        if date_to.lower() == "today":
            date_to = datetime.now().strftime(self.DATE_FORMAT)
        try:
            datetime.strptime(date_from, self.DATE_FORMAT)
            datetime.strptime(date_to, self.DATE_FORMAT)
        except ValueError:
            print("Invalid date format")
            return

        query = "SELECT * FROM time_records WHERE date BETWEEN ? AND ?"
        parameters = (date_from, date_to)
        records = self.database.execute_query(query, parameters)
        print_records(records)

    def priority(self):
        query = "SELECT task FROM time_records"
        tasks = [record[0] for record in self.database.execute_query(query)]
        task_counts = Counter(tasks)
        most_frequent_tasks = task_counts.most_common(10)

        if most_frequent_tasks:
            print("Priority tasks:")
            for task, count in most_frequent_tasks:
                if count > 1:
                    query = "SELECT * FROM time_records WHERE task = ?"
                    parameters = (task,)
                    records = self.database.execute_query(query, parameters)
                    print_records(records)
                    print(f"Total time spent on '{task}': {count} records\n")
        else:
            print("No frequent activities")

    def close(self):
        self.database.close()

    def _record_time(self, date, from_time, to_time, task, tag):
        pass


def main():
    parser = argparse.ArgumentParser(description="Time Management Tool")
    parser.add_argument("--database", default="timeManagement.db", help="Database file")
    args = parser.parse_args()

    database = Database(database_file=args.database)
    tool = TimeManagementTool(database)

    commands = {
        "record": RecordCommand(),
        "query": QueryCommand(),
        "report": ReportCommand(),
        "priority": PriorityCommand(),
    }

    print("""
    Welcome to the Time Management Application!

    To record time, use the following format:
    - record DATE FROM_TIME TO_TIME 'TASK' :TAG
    - record DATE FROM_TIME(AM/PM) TO_TIME(AM/PM) 'TASK' :TAG
    - record today FROM_TIME TO_TIME 'TASK' :TAG
    - record today FROM_TIME(AM/PM) TO_TIME(AM/PM) 'TASK' :TAG

    To query your records, you have the following options:
    - query today
    - query yyyy/mm/dd
    - query :TAG

    To print a record of activities, use the following format:
    - report yyyy/mm/dd yyyy/mm/dd

    To get a list of top 10 common activities, use command:
    - priority

    Please enter your command: (q to quit)
    """)

    while True:
        user_input = input("Enter your command: ")

        if user_input.lower() == 'q':
            tool.close()
            break

        input_values = user_input.split()
        command_name = input_values[0].lower()

        if command_name in commands:
            tool.process_command(commands[command_name], input_values[1:])
        else:
            print("Invalid command. Try again")


if __name__ == "__main__":
    main()
