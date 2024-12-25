# Dosya Şifreleme Uygulaması

Python ve PySide6 ile geliştirilmiş modern ve güvenli bir dosya şifreleme uygulaması.

## Özellikler

- 🔒 Fernet simetrik şifreleme ile dosya şifreleme
- 🔑 Parola tabanlı anahtar türetme (PBKDF2)
- 🎨 Modern ve kullanıcı dostu arayüz
- 📊 Gerçek zamanlı ilerleme takibi
- 👁 Parola görünürlük kontrolü
- 🔄 Şifreleme ve şifre çözme desteği

## Gereksinimler

- Python 3.x
- PySide6 6.6.1
- cryptography 42.0.2

## Kurulum

1. Depoyu klonlayın
```bash
git clone https://github.com/muhammedaliacis/file_encryption_app.git
cd file_encryption_app
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

2. "Dosya Seç" butonuna tıklayarak bir dosya seçin
3. Şifrenizi girin
4. Şifrelemek için "Şifrele", şifre çözmek için "Şifre Çöz" butonuna tıklayın

## Güvenlik

- Endüstri standardı şifreleme algoritmaları kullanır
- Güvenli anahtar türetme için PBKDF2 kullanır
- Şifrelenmiş dosyalar `.encrypted` uzantısı ile kaydedilir

## Ekran Görüntüleri

![Uygulama Arayüzü](screenshots/app_screenshot.png)

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylı bilgi için [LICENSE](LICENSE) dosyasına bakınız. 