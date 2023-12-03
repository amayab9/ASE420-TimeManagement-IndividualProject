# Time Management Tool
This tool is deigned to help you manage your time by recording and tracking how you use your time. This application uses command line.


## Running your program
To get started with your program, open it by navigating to the main folder of the application.

Once you are in the program folder, open a terminal and type: `python program.py`.
For commands, reference the directions that pop up in your terminal, or read below for more information on how to use the commands.
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

