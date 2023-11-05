# Time Management Application
This command-line time management application is designed to help record and manage your daily activities, track your time usage, and generate reports for better time management. The application uses Python and SQLite as the programming language and database.

## Business Logic
Jack reached out with a request to create a time management application with a CUI interface that provides flexibility in recording and query time usage. Here are the key features: 

### Recording Time
You can record your time usage using the "record" command followed by this format:

* DATE FROM_TIME TO_TIME TASK TAG

For example:

* record today 09:30 10:30 'studied Java' :STUDY

You can specify the date in the "YYYY/MM/DD" format as well as add "AM" or "PM" to the "FROM_TIME" or "TO_TIME."

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
* `report yyyy/mm/dd yyyy/mm/dd`: Retreives all records from all dates between the specified dates (inclusive)

### Priority
You can query your most frequent activity.
For example:

* `priority`: 


### Database and Language
This application is built with Python and SQLite as the standard package for the database.


