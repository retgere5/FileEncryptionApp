from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QFileDialog, 
                             QProgressBar, QMessageBox)
from PySide6.QtCore import Qt
from ..crypto.crypto_worker import CryptoWorker
from .styles import MAIN_STYLE, TITLE_STYLE, STATUS_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Dosya Şifreleme Uygulaması")
        self.setMinimumSize(800, 500)
        self.setStyleSheet(MAIN_STYLE)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        self.setup_title(layout)
        self.setup_file_selection(layout)
        self.setup_password_input(layout)
        self.setup_buttons(layout)
        self.setup_progress(layout)
        
    def setup_title(self, layout):
        title = QLabel("Dosya Şifreleme")
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

    def setup_file_selection(self, layout):
        browse_btn = QPushButton("📂 Dosya Seç")
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)
        
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Seçilen dosya yolu...")
        self.file_path.setReadOnly(True)
        layout.addWidget(self.file_path)

    def setup_password_input(self, layout):
        password_layout = QHBoxLayout()
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Şifre giriniz...")
        self.password.setEchoMode(QLineEdit.Password)
        
        self.show_password_btn = QPushButton("👁")
        self.show_password_btn.setFixedWidth(40)
        self.show_password_btn.pressed.connect(lambda: self.password.setEchoMode(QLineEdit.Normal))
        self.show_password_btn.released.connect(lambda: self.password.setEchoMode(QLineEdit.Password))
        
        password_layout.addWidget(self.password)
        password_layout.addWidget(self.show_password_btn)
        layout.addLayout(password_layout)

    def setup_buttons(self, layout):
        buttons_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton("🔒 Şifrele")
        self.decrypt_btn = QPushButton("🔓 Şifre Çöz")
        
        self.encrypt_btn.clicked.connect(lambda: self.process_file('encrypt'))
        self.decrypt_btn.clicked.connect(lambda: self.process_file('decrypt'))
        
        buttons_layout.addWidget(self.encrypt_btn)
        buttons_layout.addWidget(self.decrypt_btn)
        layout.addLayout(buttons_layout)

    def setup_progress(self, layout):
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.status_label = QLabel()
        self.status_label.setStyleSheet(STATUS_STYLE)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç")
        if file_path:
            self.file_path.setText(file_path)

    def process_file(self, operation):
        if not self.file_path.text() or not self.password.text():
            QMessageBox.warning(self, "Hata", "Lütfen dosya ve şifre giriniz!")
            return

        self.update_ui_for_processing()
        self.start_worker(operation)
        
    def update_ui_for_processing(self):
        self.encrypt_btn.setEnabled(False)
        self.decrypt_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setVisible(True)
        self.status_label.setText("İşlem başlatılıyor...")
        
    def start_worker(self, operation):
        self.worker = CryptoWorker(operation, self.file_path.text(), self.password.text())
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.process_completed)
        self.worker.error.connect(self.process_error)
        self.worker.start()

    def update_progress(self, value):
        self.progress.setValue(value)
        self.status_label.setText(f"İşlem devam ediyor... (%{value})")

    def process_completed(self, output_path):
        self.progress.setValue(100)
        self.status_label.setText("İşlem tamamlandı!")
        self.encrypt_btn.setEnabled(True)
        self.decrypt_btn.setEnabled(True)
        QMessageBox.information(self, "Başarılı", f"İşlem tamamlandı!\nDosya kaydedildi: {output_path}")

    def process_error(self, error_message):
        self.progress.setVisible(False)
        self.status_label.setVisible(False)
        self.encrypt_btn.setEnabled(True)
        self.decrypt_btn.setEnabled(True)
        QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {error_message}") 