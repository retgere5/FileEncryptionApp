import unittest
import os
import tempfile

from src.utils.file_handler import validate_file_path, get_output_path
from src.utils.error_handler import handle_crypto_error
from cryptography.fernet import InvalidToken

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Geçici test dosyası oluştur
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
    def tearDown(self):
        # Test dosyasını temizle
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
            
    def test_validate_file_path(self):
        # Var olan dosya için test
        is_valid, error = validate_file_path(self.temp_file.name)
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
        
        # Var olmayan dosya için test
        is_valid, error = validate_file_path("nonexistent_file.txt")
        self.assertFalse(is_valid)
        self.assertIn("bulunamadı", error)
        
    def test_get_output_path(self):
        # Şifreleme için çıktı yolu testi
        output_path = get_output_path("test.txt", "encrypt")
        self.assertEqual(output_path, "test.txt.encrypted")
        
        # Şifre çözme için çıktı yolu testi
        output_path = get_output_path("test.txt.encrypted", "decrypt")
        self.assertEqual(output_path, "test.txt")
        
    def test_handle_crypto_error(self):
        # InvalidToken hatası için test
        success, message = handle_crypto_error(InvalidToken())
        self.assertFalse(success)
        self.assertIn("Geçersiz şifre", message)
        
        # IOError için test
        success, message = handle_crypto_error(IOError("Test error"))
        self.assertFalse(success)
        self.assertIn("Dosya işleme hatası", message)
        
        # Genel hata için test
        success, message = handle_crypto_error(Exception("Test error"))
        self.assertFalse(success)
        self.assertIn("Beklenmeyen bir hata", message)

if __name__ == '__main__':
    unittest.main() 