# gui.py 

import tkinter as tk
from tkinter import ttk
from tokenizer import Tokenizer
from parser_module import Parser

class SyntaxHighlighterApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()  # Arayüzü kur
        self.setup_tags()  # Renk etiketlerini ayarla

    def setup_ui(self):
        """GUI bileşenlerini oluşturur ve düzenler"""
        self.root.title("Sözdizimi Vurgulayıcı")
        self.root.geometry("800x600")
        
        # Ana metin alanı
        self.text_frame = ttk.Frame(self.root)
        self.text_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.text = tk.Text(self.text_frame, wrap="word", font=("Consolas", 12))
        self.text.pack(side="left", expand=True, fill="both")
        
        # Kaydırma çubuğu
        scrollbar = ttk.Scrollbar(self.text_frame, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)
        
        # Durum çubuğu
        self.status = ttk.Label(self.root, text="Hazır", relief="sunken")
        self.status.pack(fill="x", padx=5, pady=2)
        
        # Kontrol butonları
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill="x", padx=5, pady=2)
        
        ttk.Button(self.control_frame, text="Çözümle", command=self.parse_code).pack(side="right")
        ttk.Button(self.control_frame, text="Temizle", command=self.clear_text).pack(side="right", padx=5)
        
        self.text.bind("<KeyRelease>", self.on_key_release)  # Gerçek zamanlı vurgulama

    def setup_tags(self):
        """Token türlerine göre renkleri ayarlar"""
        token_colors = {
            "KEYWORD": "black",  # Anahtar kelimeler siyah
            "IDENTIFIER": "blue",
            "NUMBER": "green",
            "STRING": "magenta",
            "SYMBOL": "orange",
            "ERROR": "red",
            "COMMENT": "gray",  # Yorumlar gri
            "UNKNOWN": "pink"
        }
        for token_type, color in token_colors.items():
            self.text.tag_configure(token_type, foreground=color)

    def on_key_release(self, event=None):
        """Klavye girişinde vurgulamayı günceller"""
        code = self.text.get("1.0", "end-1c")
        self.highlight_code(code)

    def highlight_code(self, code):
        """Kodu tokenlara ayırır ve renklendirir"""
        tokens = Tokenizer().tokenize(code)
        
        # Eski vurgulamaları temizle
        for tag in self.text.tag_names():
            if tag != "sel":
                self.text.tag_remove(tag, "1.0", "end")
        
        # Yeni tokenları vurgula
        index = "1.0"
        for token_type, token_value in tokens:
            index = self.text.search(token_value, index, stopindex="end", nocase=False)
            if not index:
                continue
            end_index = f"{index}+{len(token_value)}c"
            self.text.tag_add(token_type, index, end_index)
            index = end_index

    def parse_code(self):
        """Kodu çözümler ve hataları gösterir"""
        code = self.text.get("1.0", "end-1c")
        tokens = Tokenizer().tokenize(code)
        parser = Parser(tokens)
        
        if parser.parse():
            self.status.config(text="Çözümleme başarılı", foreground="green")
        else:
            error_msg = " | ".join(parser.errors[:3])  # İlk 3 hatayı göster
            self.status.config(text=f"Hatalar: {error_msg}", foreground="red")
            self.highlight_errors(tokens, parser.errors)

    def highlight_errors(self, tokens, errors):
        """Hatalı tokenları kırmızıyla vurgular"""
        for tag in self.text.tag_names():
            if tag == "ERROR":
                self.text.tag_remove(tag, "1.0", "end")
        
        for token_type, token_value in tokens:
            if any(token_value in err for err in errors):
                index = "1.0"
                while True:
                    index = self.text.search(token_value, index, stopindex="end")
                    if not index:
                        break
                    end_index = f"{index}+{len(token_value)}c"
                    self.text.tag_add("ERROR", index, end_index)
                    index = end_index

    def clear_text(self):
        """Metin alanını temizler"""
        self.text.delete("1.0", "end")
        self.status.config(text="Temizlendi", foreground="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlighterApp(root)
    root.mainloop()