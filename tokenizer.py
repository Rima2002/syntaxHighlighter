# tokenizer.py - tokenizer

class Tokenizer:
    def __init__(self):
        # Anahtar kelimeler
        self.KEYWORDS = {"if", "while", "print", "end", "true", "false", "else", "elif"}
        # Semboller
        self.SYMBOLS = {'=', '+', '-', '*', '/', ':', '(', ')', '<', '>', '!', '&', '|', '%', ',', ';'}
        # Boşluk karakterleri
        self.WHITESPACE = {' ', '\t', '\n'}

    def tokenize(self, code):
        """Kodu tokenlara ayırır"""
        tokens = []
        i = 0
        while i < len(code):
            char = code[i]

            # Boşlukları atla
            if char in self.WHITESPACE:
                i += 1
                continue

            # Yorum satırları
            if char == '#':
                comment_start = i
                while i < len(code) and code[i] != '\n':
                    i += 1
                tokens.append(("COMMENT", code[comment_start:i]))  # Yorum tokenı ekle
                continue

            # Sayılar (tam sayı, ondalık)
            if char.isdigit() or char == '.':
                num = ''
                has_dot = False
                start_i = i
                while i < len(code) and (code[i].isdigit() or code[i] == '.'):
                    if code[i] == '.':
                        if has_dot: break  # Birden fazla nokta olamaz
                        has_dot = True
                    num += code[i]
                    i += 1
                tokens.append(("NUMBER", num))

                # Eğer ikinci bir nokta yüzünden durduysak, idare et
                if i < len(code) and code[i] == '.':
                    tokens.append(("SYMBOL", '.'))
                    i += 1

                continue

            # Tanımlayıcılar veya anahtar kelimeler
            if char.isalpha() or char == '_':
                ident = ''
                while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                    ident += code[i]
                    i += 1
                # Anahtar kelime kontrolü
                token_type = "KEYWORD" if ident in self.KEYWORDS else "IDENTIFIER"
                tokens.append((token_type, ident))
                continue

            # Stringler
            if char in {'"', "'"}:
                quote = char
                string_val = quote
                i += 1
                closed = False
                while i < len(code):
                    if code[i] == '\\':  # Escape karakteri
                        string_val += code[i:i+2]
                        i += 2
                    elif code[i] == quote:
                        string_val += quote
                        i += 1
                        closed = True
                        break
                    else:
                        string_val += code[i]
                        i += 1
                tokens.append(("STRING", string_val) if closed else ("ERROR", string_val))
                continue

            # Çok karakterli operatörler (==, !=, &&, ||)
            if i+1 < len(code) and code[i:i+2] in {"==", "!=", "<=", ">=", "&&", "||"}:
                tokens.append(("SYMBOL", code[i:i+2]))
                i += 2
                continue

            # Tek karakterli semboller
            if char in self.SYMBOLS:
                tokens.append(("SYMBOL", char))
                i += 1
                continue

            # Bilinmeyen karakterler
            tokens.append(("UNKNOWN", char))
            i += 1

        return tokens