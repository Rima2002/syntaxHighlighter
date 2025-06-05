# main.py - Test için ana program

from tokenizer import Tokenizer
from parser_module import Parser

def main():
    # Test kodu
    code = """
    x = 3 + 4 * (2 - 1)
    if x == 7:
        print("Doğru!")
    elif x == 5:
        print("Yakın!")
    else:
        print("Yanlış!")
    end
    # Bu bir yorum
    """
    
    print("=== TOKENIZER TEST ===")
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(code)
    for token in tokens:
        print(f"{token[0]:<12}: {token[1]}")
    
    print("\n=== PARSER TEST ===")
    parser = Parser(tokens)
    if parser.parse():
        print("Çözümleme başarılı!")
    else:
        print("Çözümleme hatalı:")
        for error in parser.errors:
            print(f"- {error}")

if __name__ == "__main__":
    main()