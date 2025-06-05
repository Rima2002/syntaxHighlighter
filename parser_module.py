# parser_module.py - parser

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # Mevcut token pozisyonu
        self.errors = []  # Hatalar

    def current(self):
        """Mevcut tokenı döndürür"""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", "")

    def match(self, token_type, value=None):
        """Token eşleşmesini kontrol eder"""
        if self.pos >= len(self.tokens):
            return False
        tok_type, tok_val = self.tokens[self.pos]
        if tok_type == token_type and (value is None or tok_val == value):
            self.pos += 1
            return True
        return False

    def expect(self, token_type, value=None):
        """Token bekler, yoksa hata ekler"""
        if not self.match(token_type, value):
            current = self.current()
            self.errors.append(f"Beklenen: {token_type}{f' {value}' if value else ''}, bulunan: {current[0]} '{current[1]}'")
            return False
        return True

    def parse(self):
        """Programı çözümler"""
        self.program()
        return not self.errors  # Hata yoksa True döner

    def program(self):
        """Program -> Statement*"""
        while self.current()[0] != "EOF":
            self.statement()

    def statement(self):
        if self.match("COMMENT"):
            return
        elif self.match("IDENTIFIER"):
            self.assign_stmt()
        elif self.match("KEYWORD", "if"):
            self.if_stmt()
        elif self.match("KEYWORD", "while"):
            self.while_stmt()
        elif self.match("KEYWORD", "print"):
            self.print_stmt()
        elif self.current()[1] in ["elif", "else"]:
            # Bunlar sadece if ifadeleri içinde görünmelidir
            self.errors.append(f"'{self.current()[1]}' without matching 'if'")
            self.pos += 1
        else:
            self.errors.append(f"Beklenmeyen token: {self.current()}")
            self.pos += 1


    def assign_stmt(self):
        """Atama ifadesi"""
        self.expect("SYMBOL", "=")
        self.expr()

    def is_at_end(self):
        """Check if we've reached the end of tokens"""
        return self.pos >= len(self.tokens)
    
    def if_stmt(self):
        """If koşulu"""
        # Başlangıç ​​if koşulunu ayrıştır (parantez gerektirmeden)
        self.expr() 
        self.expect("SYMBOL", ":")
        self.block() 
        
        # Herhangi bir sayıda elif cümlesini ayrıştır
        while self.current()[1] == "elif" and not self.is_at_end():
            self.pos += 1 
            self.expr()    
            self.expect("SYMBOL", ":")
            self.block()  
        
        # İsteğe bağlı else ifadesini ayrıştır
        if self.current()[1] == "else" and not self.is_at_end():
            self.pos += 1  
            self.expect("SYMBOL", ":")
            self.block()
        
        self.expect("KEYWORD", "end")

    def while_stmt(self):
        """While döngüsü"""
        self.expr()
        self.expect("SYMBOL", ":")
        self.block()
        self.expect("KEYWORD", "end")

    def print_stmt(self):
        """Print ifadesi"""
        self.expect("SYMBOL", "(")
        self.expr()
        while self.match("SYMBOL", ","):
            self.expr()
        self.expect("SYMBOL", ")")


    def block(self):
        """Blok içindeki ifadeler"""
        while not self.is_at_end() and self.current()[1] not in ["end", "else", "elif"]:
            self.statement()

    def expr(self):
        """İfade çözümlemesi"""
        self.logical_or()

    def logical_or(self):
        """OR mantıksal operatörü"""
        self.logical_and()
        while self.match("SYMBOL", "||"):
            self.logical_and()

    def logical_and(self):
        """AND mantıksal operatörü"""
        self.equality()
        while self.match("SYMBOL", "&&"):
            self.equality()

    def equality(self):
        """Eşitlik karşılaştırmaları"""
        self.comparison()
        while self.match("SYMBOL", "==") or self.match("SYMBOL", "!="):
            self.comparison()

    def comparison(self):
        """Karşılaştırma operatörleri"""
        self.term()
        while self.match("SYMBOL", "<") or self.match("SYMBOL", ">") or \
              self.match("SYMBOL", "<=") or self.match("SYMBOL", ">="):
            self.term()

    def term(self):
        """Toplama/çıkarma"""
        self.factor()
        while self.match("SYMBOL", "+") or self.match("SYMBOL", "-"):
            self.factor()

    def factor(self):
        """Çarpma/bölme"""
        self.atom()
        while self.match("SYMBOL", "*") or self.match("SYMBOL", "/") or self.match("SYMBOL", "%"):
            self.atom()

    def atom(self):
        """Temel ifadeler"""
        if self.match("SYMBOL", "+") or self.match("SYMBOL", "-"):
            self.atom()
            return
        if (self.match("NUMBER") or
            self.match("IDENTIFIER") or
            self.match("STRING") or
            self.match("KEYWORD", "true") or
            self.match("KEYWORD", "false")):
            return
        elif self.match("SYMBOL", "("):
            self.expr()
            self.expect("SYMBOL", ")")
        else:
            self.errors.append(f"Beklenen ifade, bulunan: {self.current()}")
            self.pos += 1