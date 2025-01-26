from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, 
    QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt
import os

from ..crypto.crypto_worker import CryptoWorker
from ..utils.languages import TRANSLATIONS
from .styles import (
    DARK_THEME, LIGHT_THEME,
    get_main_style, get_title_style,
    get_status_style, get_theme_toggle_style,
    get_lang_toggle_style, get_password_toggle_style
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = DARK_THEME
        self.current_lang = "TR"
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(self.tr("app_name"))
        self.setMinimumSize(800, 500)  # Sabit pencere boyutu
        self.apply_theme()
        
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Üst bar için widget ve layout
        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Dil değiştirme butonu (sol)
        self.lang_toggle = QPushButton(self.current_lang)
        self.lang_toggle.setStyleSheet(get_lang_toggle_style(self.current_theme))
        self.lang_toggle.clicked.connect(self.toggle_language)
        
        # Tema değiştirme butonu (sağ)
        self.theme_toggle = QPushButton("🌙" if self.current_theme == DARK_THEME else "☀️")
        self.theme_toggle.setStyleSheet(get_theme_toggle_style(self.current_theme))
        self.theme_toggle.clicked.connect(self.toggle_theme)
        
        # Butonları üst bar'a ekle
        top_layout.addWidget(self.lang_toggle, alignment=Qt.AlignLeft)
        top_layout.addStretch()  # Ortadaki boşluk
        top_layout.addWidget(self.theme_toggle, alignment=Qt.AlignRight)
        
        # Üst bar'ı ana layout'a ekle
        main_layout.addWidget(top_bar)
        
        # Diğer UI elemanları
        self.setup_title(main_layout)
        self.setup_file_selection(main_layout)
        self.setup_password_input(main_layout)
        self.setup_buttons(main_layout)
        self.setup_progress(main_layout)
        
    def tr(self, key):
        """Dil çevirisi için yardımcı fonksiyon"""
        return TRANSLATIONS[self.current_lang][key]
        
    def setup_toggle_buttons(self):
        margin = 40  # layout ile aynı margin
        button_width = 32
        
        # Tema değiştirme butonu (sağ üst köşe)
        self.theme_toggle = QPushButton("🌙" if self.current_theme == DARK_THEME else "☀️")
        self.theme_toggle.setStyleSheet(get_theme_toggle_style(self.current_theme))
        self.theme_toggle.clicked.connect(self.toggle_theme)
        self.theme_toggle.setParent(self)
        self.theme_toggle.move(self.width() - (margin + button_width), margin)
        
        # Dil değiştirme butonu (sol üst köşe)
        self.lang_toggle = QPushButton(self.current_lang)
        self.lang_toggle.setStyleSheet(get_lang_toggle_style(self.current_theme))
        self.lang_toggle.clicked.connect(self.toggle_language)
        self.lang_toggle.setParent(self)
        self.lang_toggle.move(margin, margin)
        
        # Pencere yeniden boyutlandırıldığında butonların pozisyonunu güncelle
        def update_button_positions(event):
            width = event.size().width()
            self.theme_toggle.move(width - (margin + button_width), margin)
            self.lang_toggle.move(margin, margin)
            
        self.resizeEvent = update_button_positions

    def toggle_theme(self):
        self.current_theme = LIGHT_THEME if self.current_theme == DARK_THEME else DARK_THEME
        self.theme_toggle.setText("🌙" if self.current_theme == DARK_THEME else "☀️")
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(get_main_style(self.current_theme))
        if hasattr(self, 'title'):
            self.title.setStyleSheet(get_title_style(self.current_theme))
        if hasattr(self, 'status_label'):
            self.status_label.setStyleSheet(get_status_style(self.current_theme))
        if hasattr(self, 'theme_toggle'):
            self.theme_toggle.setStyleSheet(get_theme_toggle_style(self.current_theme))
        if hasattr(self, 'lang_toggle'):
            self.lang_toggle.setStyleSheet(get_lang_toggle_style(self.current_theme))
        if hasattr(self, 'show_password_btn'):
            self.show_password_btn.setStyleSheet(get_password_toggle_style(self.current_theme))

    def setup_title(self, layout):
        self.title = QLabel(self.tr("title"))
        self.title.setStyleSheet(get_title_style(self.current_theme))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

    def setup_file_selection(self, layout):
        self.browse_btn = QPushButton(self.tr("file_button"))
        self.browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_btn)
        
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText(self.tr("file_placeholder"))
        self.file_path.setReadOnly(True)
        layout.addWidget(self.file_path)

    def setup_password_input(self, layout):
        password_layout = QHBoxLayout()
        password_layout.setSpacing(0)  # Boşluğu kaldır
        password_layout.setContentsMargins(0, 0, 0, 0)  # Kenar boşluklarını kaldır
        
        self.password = QLineEdit()
        self.password.setObjectName("password")  # CSS seçici için ID ekle
        self.password.setPlaceholderText(self.tr("password_placeholder"))
        self.password.setEchoMode(QLineEdit.Password)
        
        self.show_password_btn = QPushButton("👁")
        self.show_password_btn.setStyleSheet(get_password_toggle_style(self.current_theme))
        self.show_password_btn.pressed.connect(lambda: self.password.setEchoMode(QLineEdit.Normal))
        self.show_password_btn.released.connect(lambda: self.password.setEchoMode(QLineEdit.Password))
        
        password_layout.addWidget(self.password)
        password_layout.addWidget(self.show_password_btn)
        layout.addLayout(password_layout)

    def setup_buttons(self, layout):
        buttons_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton(self.tr("encrypt_button"))
        self.decrypt_btn = QPushButton(self.tr("decrypt_button"))
        
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
        self.status_label.setStyleSheet(get_status_style(self.current_theme))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("file_select_title"),
            "",  # Başlangıç dizini
            self.tr("file_filter")  # Dosya filtresi
        )
        if file_path:
            self.file_path.setText(file_path)

    def process_file(self, operation):
        if not self.file_path.text() or not self.password.text():
            QMessageBox.warning(self, self.tr("error_title"), self.tr("input_required"))
            return

        self.update_ui_for_processing()
        self.start_worker(operation)
        
    def update_ui_for_processing(self):
        self.encrypt_btn.setEnabled(False)
        self.decrypt_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setVisible(True)
        self.status_label.setText(self.tr("processing_started"))
        
    def start_worker(self, operation):
        self.worker = CryptoWorker(operation, self.file_path.text(), self.password.text())
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.process_completed)
        self.worker.error.connect(self.process_error)
        self.worker.start()

    def update_progress(self, value):
        self.progress.setValue(value)
        self.status_label.setText(self.tr("processing").format(value))

    def process_completed(self, output_path):
        self.progress.setValue(100)
        self.status_label.setText(self.tr("completed"))
        self.encrypt_btn.setEnabled(True)
        self.decrypt_btn.setEnabled(True)
        
        QMessageBox.information(
            self,
            self.tr("success_title"),
            self.tr("success_message").format(output_path)
        )
        
        reply = QMessageBox.question(
            self,
            self.tr("delete_file_title"),
            self.tr("delete_file_message"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                os.remove(self.file_path.text())
                QMessageBox.information(
                    self,
                    self.tr("success_title"),
                    self.tr("file_deleted")
                )
                self.file_path.clear()
            except Exception as e:
                QMessageBox.warning(
                    self,
                    self.tr("warning_title"),
                    self.tr("file_delete_error").format(str(e))
                )

    def process_error(self, error_message):
        self.progress.setVisible(False)
        self.status_label.setVisible(False)
        self.encrypt_btn.setEnabled(True)
        self.decrypt_btn.setEnabled(True)
        QMessageBox.critical(self, self.tr("error_title"), error_message)

    def toggle_language(self):
        self.current_lang = "EN" if self.current_lang == "TR" else "TR"
        self.lang_toggle.setText(self.current_lang)
        self.update_texts()
        
    def update_texts(self):
        """Tüm metinleri güncelle"""
        self.setWindowTitle(self.tr("app_name"))
        self.title.setText(self.tr("title"))
        
        # Dosya seçimi ile ilgili metinler
        self.browse_btn.setText(self.tr("file_button"))
        self.file_path.setPlaceholderText(self.tr("file_placeholder"))
        
        # Şifre alanı metinleri
        self.password.setPlaceholderText(self.tr("password_placeholder"))
        
        # Ana butonların metinleri
        self.encrypt_btn.setText(self.tr("encrypt_button"))
        self.decrypt_btn.setText(self.tr("decrypt_button"))
        
        # İşlem durumu metinleri
        if self.status_label.isVisible():
            if self.progress.value() == 100:
                self.status_label.setText(self.tr("completed"))
            else:
                self.status_label.setText(self.tr("processing").format(self.progress.value())) 