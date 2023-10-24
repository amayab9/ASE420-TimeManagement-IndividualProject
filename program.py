from datetime import datetime
import sqlite3

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

while True:
    print("Enter record DATE FROM TO TASK TAG\nOR\nquery query_search (q to quit)")
    user_input = input()

    if user_input.lower() == 'q':
        break

    input_values = user_input.split()

    today = None

    if len(input_values) >= 5:
        command = input_values[0]
        if command.lower() == "record":
            user_input_date = input_values[1]
            user_input_from_time = input_values[2]
            user_input_to_time = input_values[3]

            task_tag_string = ' '.join(input_values[4:])

            task_parts = task_tag_string.split(':')

            if len(task_parts) > 1:
                user_input_task = task_parts[0].strip()
                user_input_tag = task_parts[1].strip()
            else:
                user_input_task = task_parts[0].strip()
                user_input_tag = ""

            if user_input_date.lower() == "today":
                today = datetime.now().strftime("%Y/%m/%d")
            else:
                try:
                    datetime.strptime(user_input_date, "%Y/%m/%d")
                    today = user_input_date
                except ValueError:
                    print("Invalid date format")
                    continue

            if len(input_values) >= 5:
                cursor.execute("INSERT INTO time_records (date, from_time, to_time, task, tag) VALUES (?, ?, ?, ?, ?)",
                               (today, user_input_from_time, user_input_to_time, user_input_task, user_input_tag))
                conn.commit()
                print("Record submitted successfully")
            else:
                print("Invalid input format. You can provide a tag after the task.")
        else:
            print("Invalid command. Try again")

    elif len(input_values) == 2:
        command, query_request = input_values

        if command.lower() == "query":
            if query_request.lower() == "all":
                cursor.execute("SELECT * FROM time_records")
            elif query_request.lower() == "today":
                today = datetime.now().strftime("%Y/%m/%d")
                cursor.execute("SELECT * FROM time_records WHERE date = ?", (today,))
            elif query_request.startswith(":"):
                tag = query_request[1:]
                cursor.execute("SELECT * FROM time_records WHERE LOWER(tag) = LOWER(?)", (tag,))
            else:
                cursor.execute("SELECT * FROM time_records WHERE task = ?", (query_request,))

            results = cursor.fetchall()

            if results:
                for record in results:
                    id, date, from_time, to_time, task, tag = record
                    print(f"ID: {id}, Date: {date}, From: {from_time}, To: {to_time}, Task: {task}, Tag: {tag}")
            else:
                print("No records found.")
        else:
            print("Command not recognized")

    else:
        print("Invalid input format.")

conn.close()
