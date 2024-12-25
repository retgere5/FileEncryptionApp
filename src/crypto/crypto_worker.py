from PySide6.QtCore import QThread, Signal
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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
        salt = b'fixed_salt_for_demo'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def run(self):
        try:
            self.progress.emit(10)
            key = self.get_key_from_password(self.password)
            cipher_suite = Fernet(key)
            
            self.progress.emit(30)
            
            with open(self.file_path, 'rb') as file:
                file_data = file.read()
            
            self.progress.emit(50)
            
            try:
                if self.operation == 'encrypt':
                    processed_data = cipher_suite.encrypt(file_data)
                    output_path = f"{self.file_path}.encrypted"
                else:
                    processed_data = cipher_suite.decrypt(file_data)
                    output_path = self.file_path.replace('.encrypted', '')
            except InvalidToken:
                self.error.emit("Yanlış şifre! Lütfen doğru şifreyi giriniz.")
                return
            
            self.progress.emit(75)
            
            with open(output_path, 'wb') as file:
                file.write(processed_data)
            
            self.progress.emit(100)
            self.finished.emit(output_path)
            
        except Exception as e:
            self.error.emit(str(e)) 