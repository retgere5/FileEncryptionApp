from typing import Tuple
from cryptography.fernet import InvalidToken

def handle_crypto_error(e: Exception) -> Tuple[bool, str]:
    """Şifreleme işlemi sırasında oluşan hataları yönetir."""
    if isinstance(e, InvalidToken):
        return False, "Yanlış şifre! Lütfen doğru şifreyi giriniz."
    elif isinstance(e, PermissionError):
        return False, "Dosya erişim izni reddedildi!"
    elif isinstance(e, IOError):
        return False, "Dosya okuma/yazma hatası!"
    return False, f"Beklenmeyen bir hata oluştu: {str(e)}" 