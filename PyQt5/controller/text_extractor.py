from view.main_window import MainWindow
from model.image_processing import extract_text_from_image

class Controller(MainWindow):
    def __init__(self):
        super().__init__()
        self.btn_extract_text.clicked.connect(self.on_extract_text)

    def on_extract_text(self):
        text = extract_text_from_image(self.image_path)
        self.text_edit.setText(text)