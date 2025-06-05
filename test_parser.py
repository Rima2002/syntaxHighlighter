# test_parser.py - Parser Testleri

import unittest
from tokenizer import Tokenizer
from parser_module import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def parse_code(self, code):
        tokens = self.tokenizer.tokenize(code)
        parser = Parser(tokens)
        success = parser.parse()
        return success, parser.errors

    def test_valid_if_else(self):
        code = """
        if true:
            x = 1
        elif false:
            x = 2
        else:
            x = 3
        end
        """
        success, errors = self.parse_code(code)
        self.assertTrue(success)
        self.assertEqual(errors, [])

    def test_missing_end(self):
        code = """
        if x > 0:
            x = x - 1
        """
        success, errors = self.parse_code(code)
        self.assertFalse(success)
        self.assertIn("Beklenen: KEYWORD end", errors[0])

    def test_invalid_expression(self):
        code = """
        x = * 5
        """
        success, errors = self.parse_code(code)
        self.assertFalse(success)
        self.assertTrue(any("Beklenen ifade" in err for err in errors))

    def test_nested_while(self):
        code = """
        while true:
            if x == 1:
                print("A")
            end
        end
        """
        success, errors = self.parse_code(code)
        self.assertTrue(success)
        self.assertEqual(errors, [])

if __name__ == "__main__":
    unittest.main()
