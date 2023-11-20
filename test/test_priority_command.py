import unittest
from unittest.mock import patch
from io import StringIO
from src.final_time_management_tool import Database, TimeManagementTool, PriorityCommand


class TestTimeManagementTool(unittest.TestCase):
    def setUp(self):
        self.database = Database(database_file="../test.db")
        self.tool = TimeManagementTool(self.database)

    def tearDown(self):
        self.tool.close()

    def test_priority_command(self):
        # Add some records to the database for testing
        test_input_values1 = ['today', '09:00', '12:00', 'Task A', ':TAG']
        test_input_values2 = ['today', '12:00', '14:00', 'Task B', ':TAG']
        test_input_values3 = ['2023/03/25', '08:00AM', '12:00PM', 'Task A', ':TAG']

        with patch('builtins.input', side_effect=test_input_values1):
            self.tool.record(*test_input_values1)
        with patch('builtins.input', side_effect=test_input_values2):
            self.tool.record(*test_input_values2)
        with patch('builtins.input', side_effect=test_input_values3):
            self.tool.record(*test_input_values3)

        # Run the PriorityCommand
        priority_command = PriorityCommand()
        with unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            priority_command.execute(self.tool, [])

            # Assert that the output contains the expected tasks and tags
            output = mock_stdout.getvalue()
            print("Actual Output:")
            print(output)
            self.assertIn('Task A', output)
            self.assertIn('Task B', output)
            self.assertIn(':TAG', output)


if __name__ == '__main__':
    unittest.main()

#  passed
