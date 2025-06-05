# test_tokenizer.py - Tokenizer testleri

import unittest
from tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_numbers(self):
        tokens = self.tokenizer.tokenize("123 45.67 .89 1.2.3")
        expected = [
            ("NUMBER", "123"),
            ("NUMBER", "45.67"),
            ("NUMBER", ".89"),
            ("NUMBER", "1.2"),
            ("SYMBOL", "."),
            ("NUMBER", "3")
        ]
        self.assertEqual(tokens, expected)

    def test_comments(self):
        tokens = self.tokenizer.tokenize("x=5 # Yorum satırı\ny=3")
        self.assertEqual(tokens[-1], ("NUMBER", "3"))  # Yorum sonrası token kontrolü

    def test_strings(self):
        tokens = self.tokenizer.tokenize('msg = "Merhaba dünya"')
        self.assertEqual(tokens[2], ("STRING", '"Merhaba dünya"'))

    def test_keywords(self):
        tokens = self.tokenizer.tokenize("if true else end")
        self.assertEqual(tokens[0], ("KEYWORD", "if"))  # Anahtar kelime kontrolü
        
    def test_elif_keyword(self):
        tokens = self.tokenizer.tokenize("elif x == 2:")
        self.assertEqual(tokens[0], ("KEYWORD", "elif"))

if __name__ == "__main__":
    unittest.main()