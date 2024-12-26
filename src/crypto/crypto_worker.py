from PySide6.QtCore import QThread, Signal
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

from ..utils.constants import SALT, ITERATIONS, KEY_LENGTH, HASH_ALGORITHM
from ..utils.file_handler import validate_file_path, get_output_path
from ..utils.error_handler import handle_crypto_error

class CryptoWorker(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    
    # Dosyaları bu boyutta parçalar halinde işleyeceğiz
    CHUNK_SIZE = 1024 * 1024  # 1MB

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

    def process_file_in_chunks(self, input_path, output_path, cipher_suite):
        total_size = os.path.getsize(input_path)
        bytes_processed = 0
        
        with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
            while True:
                chunk = infile.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                    
                if self.operation == 'encrypt':
                    processed_chunk = cipher_suite.encrypt(chunk)
                else:
                    processed_chunk = cipher_suite.decrypt(chunk)
                    
                outfile.write(processed_chunk)
                
                # İlerlemeyi güncelle
                bytes_processed += len(chunk)
                progress = int((bytes_processed / total_size) * 100)
                self.progress.emit(progress)

    def run(self):
        try:
            # Dosya yolunu doğrula
            is_valid, error_message = validate_file_path(self.file_path)
            if not is_valid:
                self.error.emit(error_message)
                return

            # Anahtar oluştur
            self.progress.emit(5)
            key = self.get_key_from_password(self.password)
            cipher_suite = Fernet(key)
            
            # Çıktı dosyası yolunu al
            output_path = get_output_path(self.file_path, self.operation)
            
            # Dosyayı parçalar halinde işle
            self.process_file_in_chunks(self.file_path, output_path, cipher_suite)
            
            # İşlem tamamlandı
            self.progress.emit(100)
            self.finished.emit(output_path)
            
        except Exception as e:
            _, error_message = handle_crypto_error(e)
            self.error.emit(error_message) 