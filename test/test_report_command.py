import unittest
from unittest.mock import MagicMock

from src.final_time_management_tool import ReportCommand


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


if __name__ == '__main__':
    unittest.main()
# passed
