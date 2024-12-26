from PySide6.QtCore import QThread, Signal
import base64
import os
import secrets
import ctypes
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ..utils.constants import (SALT_SIZE, ITERATIONS, KEY_LENGTH, HASH_ALGORITHM,
                           SECURE_FILE_PERMISSIONS, ERROR_MESSAGES)
from ..utils.file_handler import validate_file_path, get_output_path
from ..utils.error_handler import handle_crypto_error

class CryptoWorker(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    
    CHUNK_SIZE = 1024 * 1024  # 1MB
    FERNET_OVERHEAD = 80  # Fernet her chunk'a eklediği ekstra veri boyutu

    def __init__(self, operation, file_path, password):
        super().__init__()
        self.operation = operation
        self.file_path = file_path
        self._password = password.encode()
        self._key = None
        self._salt = None

    def __del__(self):
        self._secure_cleanup()

    def _secure_cleanup(self):
        """Hassas verileri bellekten güvenli bir şekilde temizler."""
        if hasattr(self, '_password') and self._password:
            ctypes.memset(self._password, 0, len(self._password))
            del self._password
        if hasattr(self, '_key') and self._key:
            ctypes.memset(self._key, 0, len(self._key))
            del self._key
        if hasattr(self, '_salt') and self._salt:
            ctypes.memset(self._salt, 0, len(self._salt))
            del self._salt

    def get_key_from_password(self):
        """Şifreden güvenli bir anahtar türetir."""
        try:
            if self.operation == 'encrypt':
                self._salt = secrets.token_bytes(SALT_SIZE)
            else:
                # Şifre çözme işleminde salt değerini dosyadan oku
                with open(self.file_path, 'rb') as f:
                    self._salt = f.read(SALT_SIZE)
                    if len(self._salt) != SALT_SIZE:
                        raise InvalidToken("Geçersiz şifrelenmiş dosya formatı")

            kdf = PBKDF2HMAC(
                algorithm=getattr(hashes, HASH_ALGORITHM)(),
                length=KEY_LENGTH,
                salt=self._salt,
                iterations=ITERATIONS,
            )
            return base64.urlsafe_b64encode(kdf.derive(self._password))
        except Exception as e:
            self._secure_cleanup()
            raise e

    def process_file_in_chunks(self, input_path, output_path, cipher_suite):
        """Dosyayı güvenli bir şekilde şifreler veya şifresini çözer."""
        try:
            # Dosya izinlerini ayarla
            if os.path.exists(output_path):
                os.chmod(output_path, SECURE_FILE_PERMISSIONS)

            total_size = os.path.getsize(input_path)
            bytes_processed = 0
            
            with open(input_path, 'rb') as infile:
                with open(output_path, 'wb') as outfile:
                    if self.operation == 'encrypt':
                        # Şifreleme işleminde salt değerini dosyanın başına yaz
                        outfile.write(self._salt)
                        
                        # Dosyayı şifrele
                        while True:
                            chunk = infile.read(self.CHUNK_SIZE)
                            if not chunk:
                                break
                            processed_chunk = cipher_suite.encrypt(chunk)
                            outfile.write(processed_chunk)
                            bytes_processed += len(chunk)
                            progress = int((bytes_processed / total_size) * 100)
                            self.progress.emit(progress)
                    else:
                        try:
                            # Salt değerini atla
                            infile.seek(SALT_SIZE)
                            
                            # Şifrelenmiş veriyi parçalar halinde oku ve çöz
                            encrypted_size = total_size - SALT_SIZE
                            while bytes_processed < encrypted_size:
                                # Fernet overhead'i hesaba katarak chunk boyutunu ayarla
                                chunk_with_overhead = self.CHUNK_SIZE + self.FERNET_OVERHEAD
                                encrypted_chunk = infile.read(chunk_with_overhead)
                                if not encrypted_chunk:
                                    break
                                
                                try:
                                    decrypted_chunk = cipher_suite.decrypt(encrypted_chunk)
                                    outfile.write(decrypted_chunk)
                                    bytes_processed += len(encrypted_chunk)
                                    progress = int((bytes_processed / encrypted_size) * 100)
                                    self.progress.emit(progress)
                                except InvalidToken:
                                    raise InvalidToken("Yanlış şifre veya bozuk dosya")
                                
                        except InvalidToken as e:
                            raise e

            # Çıktı dosyasının izinlerini ayarla
            os.chmod(output_path, SECURE_FILE_PERMISSIONS)

        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            raise e

    def run(self):
        try:
            # Dosya yolunu doğrula
            is_valid, error_message = validate_file_path(self.file_path)
            if not is_valid:
                self.error.emit(ERROR_MESSAGES.get("file_not_found"))
                return

            # Anahtar oluştur
            self.progress.emit(5)
            self._key = self.get_key_from_password()
            cipher_suite = Fernet(self._key)
            
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
        finally:
            self._secure_cleanup() 