MAIN_STYLE = """
    QMainWindow {
        background-color: #1a1a1a;
    }
    QWidget {
        color: #ffffff;
    }
    QLabel {
        color: #00ff9d;
        font-size: 14px;
    }
    QLineEdit {
        padding: 12px;
        background-color: rgba(42, 42, 42, 0.7);
        border: 2px solid #00ff9d;
        border-radius: 8px;
        color: white;
        font-size: 14px;
    }
    QLineEdit:focus {
        border: 2px solid #00ccff;
        background-color: rgba(42, 42, 42, 0.9);
    }
    QPushButton {
        padding: 12px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ff9d, stop:1 #00ccff);
        border: none;
        border-radius: 8px;
        color: black;
        font-weight: bold;
        font-size: 14px;
        min-width: 120px;
        margin: 2px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ccff, stop:1 #00ff9d);
        margin: 0px;
        padding: 14px;
    }
    QPushButton:pressed {
        padding: 12px;
        margin: 2px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00cc99, stop:1 #00b3e6);
    }
    QPushButton:disabled {
        background: #666666;
        color: #999999;
    }
    QProgressBar {
        border: 2px solid #00ff9d;
        border-radius: 8px;
        text-align: center;
        background-color: rgba(42, 42, 42, 0.7);
        height: 25px;
        font-weight: bold;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ff9d, stop:1 #00ccff);
        border-radius: 6px;
    }
"""

TITLE_STYLE = """
    font-size: 32px;
    font-weight: bold;
    color: #00ff9d;
    margin: 20px;
"""

STATUS_STYLE = """
    color: #00ff9d;
    font-size: 16px;
    font-weight: bold;
"""