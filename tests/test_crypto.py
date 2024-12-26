import unittest
import os
import tempfile
from src.crypto.crypto_worker import CryptoWorker

class TestCrypto(unittest.TestCase):
    def setUp(self):
        self.test_data = b"Test data for encryption"
        self.password = "test_password"
        
        # Geçici test dosyası oluştur
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(self.test_data)
        self.temp_file.close()
        
    def tearDown(self):
        # Test dosyalarını temizle
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
        if os.path.exists(f"{self.temp_file.name}.encrypted"):
            os.remove(f"{self.temp_file.name}.encrypted")
            
    def test_encryption_decryption(self):
        # Şifreleme işlemi
        encrypt_worker = CryptoWorker('encrypt', self.temp_file.name, self.password)
        encrypt_worker.run()
        
        self.assertTrue(os.path.exists(f"{self.temp_file.name}.encrypted"))
        
        # Şifre çözme işlemi
        decrypt_worker = CryptoWorker('decrypt', f"{self.temp_file.name}.encrypted", self.password)
        decrypt_worker.run()
        
        # Şifresi çözülen veriyi kontrol et
        with open(self.temp_file.name, 'rb') as f:
            decrypted_data = f.read()
        
        self.assertEqual(decrypted_data, self.test_data)
        
    def test_wrong_password(self):
        # Şifreleme işlemi
        encrypt_worker = CryptoWorker('encrypt', self.temp_file.name, self.password)
        encrypt_worker.run()
        
        # Yanlış şifre ile şifre çözme işlemi
        decrypt_worker = CryptoWorker('decrypt', f"{self.temp_file.name}.encrypted", "wrong_password")
        
        # Hata mesajını yakala
        error_message = None
        def on_error(msg):
            nonlocal error_message
            error_message = msg
            
        decrypt_worker.error.connect(on_error)
        decrypt_worker.run()
        
        self.assertIsNotNone(error_message)
        self.assertIn("Yanlış şifre", error_message)

if __name__ == '__main__':
    unittest.main() 