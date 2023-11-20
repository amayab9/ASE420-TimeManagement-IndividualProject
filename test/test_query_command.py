import unittest
from unittest.mock import MagicMock

from src.final_time_management_tool import QueryCommand


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
# all passed
