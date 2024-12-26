# Uygulama sabitleri
APP_NAME = "Dosya Şifreleme Uygulaması"
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 500

# Şifreleme sabitleri
SALT_SIZE = 32  # bytes
ITERATIONS = 310000  # OWASP 2024 tavsiyesi
KEY_LENGTH = 32
HASH_ALGORITHM = "SHA256"

# Dosya işleme sabitleri
ENCRYPTED_EXTENSION = ".encrypted"
SECURE_FILE_PERMISSIONS = 0o600  # Sadece sahibi okuyup yazabilir

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

# Genel hata mesajları
ERROR_MESSAGES = {
    "file_not_found": "Dosya bulunamadı.",
    "permission_denied": "Dosya erişim izni reddedildi.",
    "invalid_password": "Geçersiz şifre.",
    "io_error": "Dosya işleme hatası.",
    "unknown_error": "Beklenmeyen bir hata oluştu."
} 