# Dosya Şifreleme Uygulaması

Python ve PySide6 ile geliştirilmiş modern ve güvenli bir dosya şifreleme uygulaması.

## Özellikler

- 🔒 Fernet simetrik şifreleme ile dosya şifreleme
- 🔑 Parola tabanlı anahtar türetme (PBKDF2)
- 🎨 Modern ve kullanıcı dostu arayüz
- 📊 Gerçek zamanlı ilerleme takibi
- 👁 Parola görünürlük kontrolü
- 🔄 Şifreleme ve şifre çözme desteği
- 🗑️ İşlem sonrası orijinal dosyayı güvenli silme seçeneği
- 🌙 Koyu/Açık tema desteği
- 🌐 Türkçe/İngilizce dil desteği
- 🎯 Geliştirilmiş buton yerleşimi ve kullanıcı deneyimi

## Gereksinimler

- Python 3.x
- PySide6 6.6.1
- cryptography 42.0.2

## Kurulum

1. Depoyu klonlayın
```bash
git clone https://github.com/retgere5/FileEncryptionApp.git
cd FileEncryptionApp
```

2. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

## Kullanım

1. Uygulamayı çalıştırın
```bash
python main.py
```

2. İsterseniz sağ üstteki 🌙/☀️ butonu ile temayı değiştirebilirsiniz
3. Sol üstteki TR/EN butonu ile dili değiştirebilirsiniz
4. "Dosya Seç" butonuna tıklayarak bir dosya seçin
5. Şifrenizi girin (👁 butonu ile şifreyi görüntüleyebilirsiniz)
6. Şifrelemek için "Şifrele", şifre çözme için "Şifre Çöz" butonuna tıklayın
7. İşlem tamamlandıktan sonra, orijinal dosyayı silmek isteyip istemediğinizi seçin

## Güvenlik

- 🔐 Endüstri standardı şifreleme algoritmaları:
  - Fernet simetrik şifreleme (AES-128 CBC mode)
  - PBKDF2 ile güvenli anahtar türetme (SHA-256)
  - 310,000 PBKDF2 iterasyonu (OWASP 2024 tavsiyesi)
  - Her şifreleme için benzersiz 32-byte salt
  
- 🧹 Güvenli veri yönetimi:
  - Hassas verilerin bellekten güvenli temizlenmesi
  - Şifrelenmiş dosyalar için güvenli dosya izinleri
  - Orijinal dosyaları güvenli silme seçeneği

- 📁 Dosya işlemleri:
  - Büyük dosyalar için chunk-based işleme
  - Şifrelenmiş dosyalar `.encrypted` uzantısı ile kaydedilir
  - İşlem başarısız olursa yarım kalan dosyalar otomatik silinir

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylı bilgi için [LICENSE](LICENSE) dosyasına bakınız. 