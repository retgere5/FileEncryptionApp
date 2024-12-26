from typing import Tuple
import logging
from cryptography.fernet import InvalidToken
from .constants import ERROR_MESSAGES

# Logging yapılandırması
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crypto_errors.log'
)

def handle_crypto_error(e: Exception) -> Tuple[bool, str]:
    """Şifreleme işlemi sırasında oluşan hataları yönetir."""
    
    # Hatayı logla
    logging.error(f"Error occurred: {str(e)}", exc_info=True)
    
    if isinstance(e, InvalidToken):
        return False, ERROR_MESSAGES["invalid_password"]
    elif isinstance(e, PermissionError):
        return False, ERROR_MESSAGES["permission_denied"]
    elif isinstance(e, IOError):
        return False, ERROR_MESSAGES["io_error"]
    
    # Genel hatalar için teknik detayları logla ama kullanıcıya gösterme
    return False, ERROR_MESSAGES["unknown_error"] 