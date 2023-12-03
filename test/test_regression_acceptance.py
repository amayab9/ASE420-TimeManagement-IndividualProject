import unittest
from unittest.mock import patch
from io import StringIO
from src.final_time_management_tool import Database, TimeManagementTool, QueryCommand, ReportCommand, PriorityCommand, \
    RecordCommand


class TestTimeManagementTool(unittest.TestCase):
    def setUp(self):
        self.database = Database(database_file="test_time_management.db")
        self.tool = TimeManagementTool(self.database)
        self.database.execute_query("DELETE FROM time_records")

    def tearDown(self):
        self.database.close()

    def test_record_command(self):
        command = RecordCommand()
        input_values = ["2023/12/01", "10:00", "12:00", "Task", ":Tag"]

        with patch("builtins.input", side_effect=input_values):
            command.execute(self.tool, input_values)

        query = "SELECT * FROM time_records WHERE task = ?"
        parameters = ("Task",)
        records = self.database.execute_query(query, parameters)
        self.assertEqual(len(records), 1)

    def test_query_command(self):
        self.tool.record("2023/12/02", "08:00", "10:00", "Task1", ":Tag1")
        self.tool.record("2023/12/02", "12:00", "14:00", "Task2", ":Tag2")

        command = QueryCommand()
        input_values = ["2023/12/02"]

        with patch("builtins.input", side_effect=input_values):
            command.execute(self.tool, input_values)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.tool.query_records(input_values[0])
            output = mock_stdout.getvalue()

        self.assertIn("Task1", output)
        self.assertIn("Task2", output)

    def test_report_command(self):
        self.tool.record("2023/12/01", "10:00", "12:00", "Task1", ":Tag1")
        self.tool.record("2023/12/01", "14:00", "16:00", "Task2", ":Tag1")
        self.tool.record("2023/12/02", "18:00", "20:00", "Task3", ":Tag2")
        self.tool.record("2023/12/02", "08:00", "10:00", "Task4", ":Tag2")

        command = ReportCommand()
        date_from = "2023/12/01"
        date_to = "2023/12/02"
        input_values = [date_from, date_to]

        with patch("builtins.input", side_effect=input_values):
            command.execute(self.tool, input_values)

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.tool.report_generator(date_from, date_to)
            output = mock_stdout.getvalue()

        self.assertIn("Task1", output)
        self.assertIn("Task2", output)
        self.assertIn("Task3", output)
        self.assertIn("Task4", output)


class TestPriorityCommand(unittest.TestCase):
    def setUp(self):
        self.database = Database(database_file="test.db")
        self.tool = TimeManagementTool(self.database)

    def tearDown(self):
        self.tool.close()

    def test_priority_command(self):
        test_input_values1 = ['today', '09:00', '12:00', 'Task A', ':TAG']
        test_input_values2 = ['today', '12:00', '14:00', 'Task B', ':TAG']
        test_input_values3 = ['2023/03/25', '08:00AM', '12:00PM', 'Task A', ':TAG']

        with patch('builtins.input', side_effect=test_input_values1):
            self.tool.record(*test_input_values1)
        with patch('builtins.input', side_effect=test_input_values2):
            self.tool.record(*test_input_values2)
        with patch('builtins.input', side_effect=test_input_values3):
            self.tool.record(*test_input_values3)

        priority_command = PriorityCommand()
        with unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            priority_command.execute(self.tool, [])

            output = mock_stdout.getvalue()
            print("Actual Output:")
            print(output)
            self.assertIn('Task A', output)
            self.assertIn('Task B', output)
            self.assertIn(':TAG', output)


if __name__ == "__main__":
    unittest.main()
