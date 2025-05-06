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

    def test_invalid_number(self):
        self.assertFalse(mock_parse_temp_command("SET TEMP -10"))

    def test_non_numeric(self):
        self.assertFalse(mock_parse_temp_command("SET TEMP abc"))

    def test_missing_value(self):
        self.assertFalse(mock_parse_temp_command("SET TEMP"))

if __name__ == '__main__':
    unittest.main()
