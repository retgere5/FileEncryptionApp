# Tema renkleri
DARK_THEME = {
    "bg_color": "#1a1a1a",
    "text_color": "#ffffff",
    "accent_color": "#00ff9d",
    "accent_color2": "#00ccff",
    "input_bg": "rgba(42, 42, 42, 0.7)",
    "disabled_bg": "#666666",
    "disabled_text": "#999999"
}

LIGHT_THEME = {
    "bg_color": "#f5f5f5",
    "text_color": "#333333",
    "accent_color": "#00cc7a",
    "accent_color2": "#0099cc",
    "input_bg": "rgba(230, 230, 230, 0.7)",
    "disabled_bg": "#cccccc",
    "disabled_text": "#666666"
}

def get_main_style(theme):
    return f"""
    QMainWindow {{
        background-color: {theme["bg_color"]};
    }}
    QWidget {{
        color: {theme["text_color"]};
    }}
    QLabel {{
        color: {theme["accent_color"]};
        font-size: 14px;
    }}
    QLineEdit {{
        padding: 12px;
        background-color: {theme["input_bg"]};
        border: 2px solid {theme["accent_color"]};
        border-radius: 8px;
        color: {theme["text_color"]};
        font-size: 14px;
        margin: 0px;
    }}
    QLineEdit:focus {{
        border: 2px solid {theme["accent_color2"]};
        background-color: {theme["input_bg"]};
    }}
    #password {{
        border-top-right-radius: 0px;
        border-bottom-right-radius: 0px;
    }}
    QPushButton {{
        padding: 12px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                  stop:0 {theme["accent_color"]}, 
                                  stop:1 {theme["accent_color2"]});
        border: none;
        border-radius: 8px;
        color: {theme["bg_color"]};
        font-weight: bold;
        font-size: 14px;
        min-width: 120px;
        margin: 2px;
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                  stop:0 {theme["accent_color2"]}, 
                                  stop:1 {theme["accent_color"]});
        margin: 0px;
        padding: 14px;
    }}
    QPushButton:pressed {{
        padding: 12px;
        margin: 2px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                  stop:0 {theme["accent_color"]}, 
                                  stop:1 {theme["accent_color2"]});
    }}
    QPushButton:disabled {{
        background: {theme["disabled_bg"]};
        color: {theme["disabled_text"]};
    }}
    QProgressBar {{
        border: 2px solid {theme["accent_color"]};
        border-radius: 8px;
        text-align: center;
        background-color: {theme["input_bg"]};
        height: 25px;
        font-weight: bold;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                  stop:0 {theme["accent_color"]}, 
                                  stop:1 {theme["accent_color2"]});
        border-radius: 6px;
    }}
"""

def get_title_style(theme):
    return f"""
    font-size: 32px;
    font-weight: bold;
    color: {theme["accent_color"]};
    margin: 20px;
"""

def get_status_style(theme):
    return f"""
    color: {theme["accent_color"]};
    font-size: 16px;
    font-weight: bold;
"""

def get_toggle_button_base_style(theme):
    return f"""
    QPushButton {{
        background-color: {theme["accent_color"]};
        border: none;
        border-radius: 6px;
        min-width: 32px;
        max-width: 32px;
        min-height: 32px;
        max-height: 32px;
        margin: 10px;
        padding: 0px;
        font-size: 14px;
        line-height: 32px;
        text-align: center;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {theme["accent_color2"]};
    }}
"""

def get_theme_toggle_style(theme):
    base_style = get_toggle_button_base_style(theme)
    return base_style.replace("font-size: 14px", "font-size: 18px")  # Emoji için daha büyük font

def get_lang_toggle_style(theme):
    return get_toggle_button_base_style(theme)

def get_password_toggle_style(theme):
    return f"""
    QPushButton {{
        background-color: {theme["accent_color"]};
        border: 2px solid {theme["accent_color"]};
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
        min-width: 40px;
        max-width: 40px;
        min-height: 45px;
        max-height: 45px;
        padding: 0px;
        font-size: 18px;
        line-height: 45px;
        text-align: center;
        margin: 0px;
        color: {theme["bg_color"]};
    }}
    QPushButton:hover {{
        background-color: {theme["accent_color2"]};
        border-color: {theme["accent_color2"]};
    }}
"""