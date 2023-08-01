from scrapper.scrapper import validate_process_number
import unittest


class TestProcessNumberValidation(unittest.TestCase):
    def test_valid_process_number(self):
        valid_process_number = "0710802-55.2018.8.02.0001"
        self.assertTrue(validate_process_number(valid_process_number))

    def test_invalid_process_number(self):
        invalid_process_number = "1234567-89.2021.0.00.0000"
        self.assertFalse(validate_process_number(invalid_process_number))

    def test_invalid_process_number(self):
        invalid_process_number = "Roberto Carlos"
        self.assertFalse(validate_process_number(invalid_process_number))


if __name__ == "__main__":
    unittest.main()
