from unittest.mock import patch
from unittest.mock import MagicMock
from src.final_time_management_tool import Database, TimeManagementTool, QueryCommand, ReportCommand, \
    PriorityCommand
import unittest
from unittest.mock import patch
from io import StringIO


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


class TestRecordCommand(unittest.TestCase):
    def setUp(self):
        self.database = Database(database_file="test.db")
        self.tool = TimeManagementTool(self.database)

    def tearDown(self):
        self.tool.close()

    def test_record_today(self):
        test_input_values_today = ['today', '09:00', '12:00', 'Task 1', ':TAG1']

        with patch('builtins.input', side_effect=test_input_values_today):
            self.tool.record(*test_input_values_today)

        with patch('builtins.input', return_value='today'), \
                unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.tool.query_records('today')

            output = mock_stdout.getvalue()
            self.assertIn('Task 1', output)
            self.assertIn(':TAG1', output)

    def test_record_date(self):
        test_input_values_date = ['2023/03/25', '08:00AM', '12:00PM', 'Task 2', ':TAG2']

        with patch('builtins.input', side_effect=test_input_values_date):
            self.tool.record(*test_input_values_date)

        with patch('builtins.input', return_value='2023/03/25'), \
                unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.tool.query_records('2023/03/25')

            output = mock_stdout.getvalue()
            self.assertIn('Task 2', output)
            self.assertIn(':TAG2', output)


class TestTimeManagementTool(unittest.TestCase):
    def setUp(self):
        self.database = Database(database_file="test.db")
        self.tool = TimeManagementTool(self.database)

    def tearDown(self):
        self.tool.close()

    def test_record(self):
        test_input_values = ['today', '09:00', '12:00', 'Task 1', ':Tag']

        with patch('builtins.input', side_effect=test_input_values):
            self.tool.record(*test_input_values)

        with patch('builtins.input', return_value='today'):
            self.tool.query_records('today')

        with unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.tool.query_records('today')

        output = mock_stdout.getvalue()
        self.assertIn('Task 1', output)
        self.assertIn(':Tag', output)


class TestReportCommand(unittest.TestCase):
    def setUp(self):
        self.mock_tool = MagicMock()
        self.report_command = ReportCommand()

    def test_execute_method(self):
        date_from = "2023/11/01"
        date_to = "2023/11/15"
        input_values = [date_from, date_to]

        self.report_command.execute(self.mock_tool, input_values)
        self.mock_tool.report_generator.assert_called_once_with(date_from, date_to)


class TestQueryCommand(unittest.TestCase):
    def setUp(self):
        self.mock_tool = MagicMock()
        self.query_command = QueryCommand()

    def test_query_by_date(self):
        query_request = "2023/11/01"
        input_values = [query_request]

        self.query_command.execute(self.mock_tool, input_values)
        self.mock_tool.query_records.assert_called_once_with(query_request)

    def test_execute_method_query_by_tag(self):
        query_request = ":work"
        input_values = [query_request]

        self.query_command.execute(self.mock_tool, input_values)
        self.mock_tool.query_records.assert_called_once_with(query_request)

    def test_execute_method_query_by_task(self):
        query_request = "Task"
        input_values = [query_request]

        self.query_command.execute(self.mock_tool, input_values)
        self.mock_tool.query_records.assert_called_once_with("Task")

    def test_execute_method_query_today(self):
        query_request = "today"
        input_values = [query_request]

        self.query_command.execute(self.mock_tool, input_values)
        self.mock_tool.query_records.assert_called_once()


if __name__ == '__main__':
    unittest.main()
