from PySide6.QtCore import QThread, Signal
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ..utils.constants import SALT, ITERATIONS, KEY_LENGTH, HASH_ALGORITHM
from ..utils.file_handler import validate_file_path, get_output_path
from ..utils.error_handler import handle_crypto_error

class CryptoWorker(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, operation, file_path, password):
        super().__init__()
        self.operation = operation
        self.file_path = file_path
        self.password = password

    def get_key_from_password(self, password):
        kdf = PBKDF2HMAC(
            algorithm=getattr(hashes, HASH_ALGORITHM)(),
            length=KEY_LENGTH,
            salt=SALT,
            iterations=ITERATIONS,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def run(self):
        try:
            # Dosya yolunu doğrula
            is_valid, error_message = validate_file_path(self.file_path)
            if not is_valid:
                self.error.emit(error_message)
                return

            self.progress.emit(10)
            key = self.get_key_from_password(self.password)
            cipher_suite = Fernet(key)
            
            self.progress.emit(30)
            
            with open(self.file_path, 'rb') as file:
                file_data = file.read()
            
            self.progress.emit(50)
            
            if self.operation == 'encrypt':
                processed_data = cipher_suite.encrypt(file_data)
            else:
                processed_data = cipher_suite.decrypt(file_data)
            
            self.progress.emit(75)
            
            output_path = get_output_path(self.file_path, self.operation)
            with open(output_path, 'wb') as file:
                file.write(processed_data)
            
            self.progress.emit(100)
            self.finished.emit(output_path)
            
        except Exception as e:
            _, error_message = handle_crypto_error(e)
            self.error.emit(error_message) 