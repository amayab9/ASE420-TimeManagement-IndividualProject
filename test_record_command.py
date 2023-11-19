import unittest
from unittest.mock import patch
from io import StringIO
from program import Database, TimeManagementTool


class TestTimeManagementTool(unittest.TestCase):
    def setUp(self):
        self.database = Database(database_file="test.db")
        self.tool = TimeManagementTool(self.database)

    def tearDown(self):
        self.tool.close()

    def test_record_today(self):
        test_input_values_today = ['today', '09:00', '12:00', 'Task 1', ':TAG1']

        # Test recording a task for today
        with patch('builtins.input', side_effect=test_input_values_today):
            self.tool.record(*test_input_values_today)

        # query the records to check if the task is properly recorded for today
        with patch('builtins.input', return_value='today'), \
                unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.tool.query_records('today')

            # Assert that the recorded task for today is in the result
            output = mock_stdout.getvalue()
            self.assertIn('Task 1', output)
            self.assertIn(':TAG1', output)

    def test_record_date(self):
        test_input_values_date = ['2023/03/25', '08:00AM', '12:00PM', 'Task 2', ':TAG2']

        # Test recording a task for date
        with patch('builtins.input', side_effect=test_input_values_date):
            self.tool.record(*test_input_values_date)

        # query the records to check if the task is properly recorded for  date
        with patch('builtins.input', return_value='2023/03/25'), \
                unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.tool.query_records('2023/03/25')

            # Assert that the recorded task for date is in the result
            output = mock_stdout.getvalue()
            self.assertIn('Task 2', output)
            self.assertIn(':TAG2', output)


if __name__ == '__main__':
    unittest.main()
# passed
