# Time Management Application
This command-line time management application is designed to help record and manage your daily activities, track your time usage, and generate reports for better time management. The application uses Python and SQLite as the programming language and database.

## Business Logic
Jack reached out with a request to create a time management application with a CUI interface that provides flexibility in recording and query time usage. Here are the key features: 

### Recording Time
You can record your time usage using the "record" command followed by this format:

* `record DATE FROM_TIME(AM/PM) TO_TIME(AM/PM) 'TASK' :TAG` : Records the date, time, task, and tag in database. For example: record today 09:30AM 10:30AM 'studied Java' :STUDY

_Shortcuts and alternatives:_
The user can use shortcuts to make the command easier to type.

* `today:` Records today's date. Use in place of DATE

_Alternatives:_
The user can also enter data in the following alternative ways without receiving an error:

* `FROM_TIME:` User can enter time of day without AM/PM if user prefers using military time.
* `TO_TIME:` User can enter time of day without AM/PM if user prefers using military time.


### Query Data
You can query your time usage using date, task, or tag.
For example:

* `query today`: Retrieves all your activity for today.
* `query 'Java'`: Retrieves all Java-related activites.
* `query :STUDY`: Retrieves all avtivites with the tag ":STUDY"

### Query Report
You can query a report of your time usage from specified dates.
For example:

* `report yyyy/mm/dd today`: Retrieves all records from the specified date to today's date
* `report yyyy/mm/dd yyyy/mm/dd`: Retrieves all records from all dates between the specified dates (inclusive)

### Priority
You can query your most frequent activity.
For example:

* `priority`: Retrieves top 10 most done activities and displays them in order from most-done to least-done with the 'task' & 'number of instances.'


### Database and Language
This application is built with Python and SQLite as the standard package for the database.


#### **Rationale
Because this is an assignment for ASE 420, we have no direct communication with the client. Below is a list of rationales for features the user wanted in the program in the format of requirement: rationale.

* `“query ‘Java’ ” to get all the Java-related activities:` The user should type only one word to display all relevant activities. In this example, the user only types "java" after query to get all Java related activities. The user should not type an unnecessary amount of information when querying information.
* `I can specify the date using the 2022/09/23 form and add AM or PM to the FROM or TO:` The user should add AM or PM to the end of the time without a space because in a command line, it is unnecessary to add a space between the time and the time of day.
* `the priority command gives me the list of activities I spend most of my time on:` Since we do not know how many activities the user will input in total, I capped the output of most common activities to 10. When the user has activities that are not done more than once, the user will not receive this task on the list. Priority will list all occurrences of the activity and the count for convenience. 

