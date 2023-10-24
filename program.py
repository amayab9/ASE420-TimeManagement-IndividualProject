from datetime import datetime
import sqlite3
from datetime import date

conn = sqlite3.connect("timeManagement.db")
cursor = conn.cursor()

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
conn.commit()


print("Enter record DATE FROM TO TASK TAG")
user_input = input()

input_values = user_input.split()

today = date.today()

if len(input_values) == 2:
    command, query_request = input_values


if len(input_values) == 6:
    command, user_input_date, user_input_from_time, user_input_to_time, user_input_task, user_input_tag = input_values
    try:
        user_input_date = datetime.strptime(user_input_date, "%Y/%m/%d").date()

        if command.lower() == "record":

            if user_input_date.lower() == "today":
                user_input_date = today

                cursor.execute("INSERT INTO time_records (date, from_time, to_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                               (user_input_date, user_input_from_time, user_input_to_time, user_input_task, user_input_tag))
                conn.commit()
                print("Record submitted successfully")
            else:
                print("invalid")
        else:
            print("Invalid command. Try again")
    except ValueError:
        print("invalid date format")

else:
    print("Invalid input format.")

cursor.execute("SELECT * FROM time_records")
records = cursor.fetchall()


if records:
    for record in records:
        id, date, from_time, to_time, task, tag = record
        task = task.strip("'")
        print(f"ID: {id}, Date: {date}, From: {from_time}, To: {to_time}, Task: {task}, Tag: {tag}")
else:
    print("No records found.")


conn.close()