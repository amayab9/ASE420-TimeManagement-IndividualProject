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

    def test_query_records(self):
        # Add record for testing
        test_record_values = ['2023/01/01', '10:00', '11:00', 'Test Task', ':Test']
        with patch('builtins.input', side_effect=test_record_values):
            self.tool.record(*test_record_values)

        # Query records for the added record
        with patch('builtins.input', return_value='Test Task'), \
                unittest.mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.tool.query_records('Test Task')
            output = mock_stdout.getvalue()
            self.assertIn('Test Task', output)
            self.assertIn(':Test', output)


if __name__ == '__main__':
    unittest.main()
