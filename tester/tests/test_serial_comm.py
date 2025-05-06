import unittest

def mock_parse_temp_command(command):
    try:
        if not command.startswith("SET TEMP "):
            return False
        value = int(command[9:])
        return 0 <= value <= 100
    except:
        return False

class TestCommandParsing(unittest.TestCase):
    def test_valid_command(self):
        self.assertTrue(mock_parse_temp_command("SET TEMP 25"))

    def test_edge_min(self):
        self.assertTrue(mock_parse_temp_command("SET TEMP 0"))

    def test_edge_max(self):
        self.assertTrue(mock_parse_temp_command("SET TEMP 100"))

    def test_invalid_number(self):
        self.assertFalse(mock_parse_temp_command("SET TEMP -10"))

    def test_above_range(self):
        self.assertFalse(mock_parse_temp_command("SET TEMP 150"))

    def test_non_numeric(self):
        self.assertFalse(mock_parse_temp_command("SET TEMP abc"))

    def test_missing_value(self):
        self.assertFalse(mock_parse_temp_command("SET TEMP"))

    def test_garbage_input(self):
        self.assertFalse(mock_parse_temp_command("!!!@@@###"))

    def test_empty_string(self):
        self.assertFalse(mock_parse_temp_command(""))

if __name__ == '__main__':
    unittest.main()
