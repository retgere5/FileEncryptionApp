# Uygulama sabitleri
APP_NAME = "Dosya Şifreleme Uygulaması"
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 500

# Şifreleme sabitleri
SALT = b'fixed_salt_for_demo'
ITERATIONS = 100000
KEY_LENGTH = 32
HASH_ALGORITHM = "SHA256"

# Dosya işleme sabitleri
ENCRYPTED_EXTENSION = ".encrypted"

# UI sabitleri
TITLE_TEXT = "Dosya Şifreleme"
FILE_BUTTON_TEXT = "📂 Dosya Seç"
FILE_PLACEHOLDER = "Seçilen dosya yolu..."
PASSWORD_PLACEHOLDER = "Şifre giriniz..."
ENCRYPT_BUTTON_TEXT = "🔒 Şifrele"
DECRYPT_BUTTON_TEXT = "🔓 Şifre Çöz"
PROCESSING_TEXT = "İşlem devam ediyor... (%{})"
COMPLETED_TEXT = "İşlem tamamlandı!"
ERROR_TITLE = "Hata"
SUCCESS_TITLE = "Başarılı"
SUCCESS_MESSAGE = "İşlem tamamlandı!\nDosya kaydedildi: {}" 