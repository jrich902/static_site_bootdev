import unittest
import os
from main import extract_title


class TestMainNode(unittest.TestCase):
    def setUp(self):
        self.test_file = "test.md"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_extract_title_success(self):

        with open(self.test_file, "w") as file:
            file.write("# Hello World")

        result = extract_title(self.test_file)

        self.assertEqual(result, "Hello World")

    def test_extract_title_no_header(self):

        with open(self.test_file, "w") as file:
            file.write("This is not a header")

        with self.assertRaises(Exception):
            extract_title(self.test_file)


if __name__ == "__main__":
    unittest.main()
