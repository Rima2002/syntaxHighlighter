# Gerçek Zamanlı Biçimbilgisel Temelli Sözdizimi Vurgulama Arayüzü

## Yazar

**Rima Farah Eleuch**  
Öğrenci Numarası: 21360859216

[Article](https://www.linkedin.com/feed/update/urn:li:activity:7336762323581255682/)

[Video: Proje Tanıtımı](https://www.youtube.com/watch?v=FuZdU7YXM8Y)

---

## Kullanılan Programlama Dili ve Araçlar

- **Programlama Dili**: Python 3.11  
- **Geliştirme Ortamı**: PyCharm, Jupyter Notebook (ilk taslaklar için)  
- **GUI Kütüphanesi**: Tkinter (Python standart kütüphanesi)  
- **Test Kütüphanesi**: unittest

---

## Dil ve Gramer Seçimi

Projede basitleştirilmiş bir programlama dili tasarladım. Desteklenen yapılar:

- Atama ifadeleri  
- Aritmetik ifadeler  
- Mantıksal ifadeler  
- `if`, `elif`, `else`, `while` blokları  
- `print()` fonksiyonu  
- Blokları kapatmak için `end` kullanımı  
- `#` ile başlayan yorum satırları  

### Örnek Kod:
```python
x = 3 + 4 * (2 - 1)

if x == 7:
    print("Doğru")
else:
    print("Yanlış")
end
```

Gramer, manuel analiz kolaylığı sağlamak üzere tasarlanmış olup temel sözdizim analizine olanak tanır.

---

## Sözdizimi (Syntax) Analizi Süreci

### Genel Yaklaşım:

- **Yöntem**: Üstten-Aşağı (Top-Down) Özyinelemeli (Recursive Descent) analiz
- **Avantaj**: Parser üreticisine ihtiyaç duymaz

### Gramer Taslağı:
```
Program     -> Statement*
Statement   -> Assignment | IfStmt | WhileStmt | PrintStmt | COMMENT
Assignment  -> IDENTIFIER '=' Expression
IfStmt      -> 'if' Expression ':' Block ( 'elif' Expression ':' Block )* ( 'else' ':' Block )? 'end'
WhileStmt   -> 'while' Expression ':' Block 'end'
PrintStmt   -> 'print' '(' Expression (',' Expression)* ')'
Block       -> Statement*
Expression  -> LogicalOr
...
```

- Parser eksik `end` ifadelerini ve yanlış `elif`/`else` kullanımını tespit eder.

---

## Sözcüksel (Lexical) Analiz Detayları

### Kullanılan Yaklaşım:

- **Uygulama**: `tokenizer.py` dosyasında  
- Durum diyagramı ve programatik kurallar temelli lexer  
- Dış kütüphane kullanılmamıştır

### Token Türleri:

- **KEYWORD**: if, else, elif, while, end, print, true, false  
- **IDENTIFIER**: değişken adları (ör. `x`, `toplam`)  
- **NUMBER**: tam sayı ve ondalık  
- **STRING**: tırnaklı string ifadeler  
- **SYMBOL**: `=`, `+`, `:`, `==`, `||`, vb.  
- **COMMENT**: `#` ile başlayan yorumlar  
- **ERROR**: hatalı stringler  
- **UNKNOWN**: bilinmeyen karakterler

### Uç Durumlar:

- Kaçış karakterli stringler  
- Çok noktalı sayılar (`1.2.3`)  
- Yorumlar token olarak korunur

---

## Ayrıştırma (Parsing) Yöntemi

- **Yöntem**: Top-Down Recursive Descent Parser  
- **Uygulama**: `parser_module.py` dosyasında  
- Lexer'dan alınan token listesiyle çalışır  
- Fonksiyonlar gramer kurallarını temsil eder: `expr()`, `if_stmt()`, vb.

### Hata Yönetimi:

- Beklenmeyen token’lar için hata mesajları listeye eklenir  
- GUI’de yalnızca ilk 3 hata gösterilir

### Özel Durumlar:

- `elif`, `else` sadece `if` bloğu içinde geçerlidir  
- `end` ifadesi zorunludur (`if` ve `while` için)

---

## Vurgulama Şeması

- `tk.Text` widget'ın etiketleme sistemi kullanılmıştır.

### Token Türleri ve Renkleri:

| Token Türü | Renk     |
|------------|----------|
| KEYWORD    | Siyah    |
| IDENTIFIER | Mavi     |
| NUMBER     | Yeşil    |
| STRING     | Magenta  |
| SYMBOL     | Turuncu  |
| COMMENT    | Gri      |
| ERROR      | Kırmızı  |
| UNKNOWN    | Pembe    |

### Gerçek Zamanlı Özellik:

- Her tuş bırakıldığında içerik yeniden tokenize edilir  
- Tüm metin baştan taranarak renklendirilir

### Performans:

- Kısa kodlar için yeterlidir (~100 satır)  
- Uzun dosyalarda optimize edilmemiştir (bu proje için kabul edilebilir)

---

## Grafik Arayüz (GUI) Uygulaması

- **Uygulama**: `gui.py` dosyasında  
- Geliştirme: `tkinter` kullanılarak  
- Özellikler:
  - Kod yazma alanı
  - Kaydırma çubuğu
  - Gerçek zamanlı vurgulama

### Düğmeler:

- **Çözümle**: Parser çalıştırır, hataları gösterir  
- **Temizle**: Alanı temizler  
- **Durum Çubuğu**: Mesaj gösterir

### Dosya: `gui.py`

#### Fonksiyonlar:

- `setup_ui()`: Arayüz bileşenlerini kurar  
- `highlight_code()`: Token'lara göre renklendirme  
- `parse_code()`: Parser çalıştırma ve hata gösterimi

### Sınırlar:

- Dosya aç/kaydet yok  
- Otomatik girintileme/sekmeler yok

---

## Testler

Testler aşağıdaki dosyalarda yer alır:

- `test_tokenizer.py`: Lexer testleri  
- `test_parser.py`: Syntax testleri (iç içe bloklar, eksik `end`, vb.)

> Testler `unittest` kullanılarak otomatikleştirilmiştir.

---

## Bilinen Sorunlar / Gelecek Geliştirmeler

- Uzun girdilerde vurgulama yavaşlayabilir  
- İfade hatası kurtarma geliştirilebilir  
- Dosya aç/kaydet eklenebilir  
- Otomatik girintileme ve kod tamamlayıcı entegre edilebilir

---

## Sonuç

Bu proje, hiçbir harici kütüphane kullanılmadan geliştirilen, gerçek zamanlı sözdizimi vurgulama uygulamasıdır. Temel ayrıştırma ve vurgulama prensipleri başarıyla uygulanmıştır.


## Kaynakça
- Aho, A. V., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2. baskı). Pearson Education.
> Projede kullandığım sözcüksel analiz ve sözdizimsel çözümleme yöntemlerinin temelini bu kitap oluşturdu. Recursive descent parser mantığı da burada açıklanıyor.

- Python Software Foundation. (2024). Python 3.11 Resmi Belgeleri. https://docs.python.org/3.11/
> Python diline ait sözdizimi, Tkinter arayüz bileşenleri ve genel kullanım detaylarını bu dokümantasyondan takip ettim.

- TkDocs. (2024). Tkinter Kullanım Kılavuzu. https://tkdocs.com/tutorial/
> Arayüz geliştirirken Text widget'ı, olay dinleyicileri ve görsel düzen hakkında bilgi almak için bu kaynaktan faydalandım.

- Grune, D., & arkadaşları. (2012). Modern Compiler Design. Springer.
> Gramer tanımı, blok yapılar ve dil çözümleme teknikleri konusunda detaylı bilgi veren, başvurulacak kaynaklardan biri.
