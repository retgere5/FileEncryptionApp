import os
from typing import Tuple

def validate_file_path(file_path: str) -> Tuple[bool, str]:
    """Dosya yolunu doğrular."""
    if not os.path.exists(file_path):
        return False, "Dosya bulunamadı!"
    if not os.path.isfile(file_path):
        return False, "Seçilen yol bir dosya değil!"
    return True, ""

def get_output_path(file_path: str, operation: str) -> str:
    """İşlem sonucu için çıktı dosyası yolunu oluşturur."""
    if operation == 'encrypt':
        return f"{file_path}.encrypted"
    return file_path.replace('.encrypted', '') 