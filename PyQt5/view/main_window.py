import os
from PyQt5 import (
    QtWidgets,
    QtGui,
    QtCore
)
from PyQt5.QtWidgets import (
    QFileDialog,
    QTextEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QApplication,
    QGridLayout,
    QMessageBox,
    QProgressBar,
    QMenuBar
)

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QPixmap


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1550, 830)
        #Enable Drag&Drop
        self.setAcceptDrops(True) 

        # Add text to image_label (Drag&Drop)
        self.image_label = QtWidgets.QLabel('Drag & Drop\nHere', self)
        self.image_label.setGeometry(290, 325, 150, 150)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setAcceptDrops(True)
        self.image_label.setStyleSheet('border: 5px dashed white')

        # Setting up paths for icons and favicon
        current_path = os.path.dirname(os.path.abspath(__file__))
        icon_folder_path = os.path.join(current_path, "..", "resources", "icons")
        favicon_folder_path = os.path.join(current_path, "..", "resources", "favicon")
        favicon_path = os.path.join(favicon_folder_path, "favicon.ico")
        open_icon_path = os.path.join(icon_folder_path, "open.png")
        save_icon_path = os.path.join(icon_folder_path, "save.png")
        extract_icon_path = os.path.join(icon_folder_path, "extract.png")
        capture_icon_path = os.path.join(icon_folder_path, "capture.png")
        about_icon_path = os.path.join(icon_folder_path, "info.png")
        
        # Setting up timer for text extraction
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.extract_text)
        
        # Setting up progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        
        # Setting up menu bar and actions
        self.menu_bar = QMenuBar(self)

        file_menu = self.menu_bar.addMenu("File")
        help_menu = self.menu_bar.addMenu("Help")


        #open_action = self.menu_bar.addAction("Open")
        open_action = file_menu.addAction("Open")
        open_action.setShortcut("Ctrl+O")
        save_action = file_menu.addAction("Save")
        save_action.setShortcut("Ctrl+S")
        extract_action = self.menu_bar.addAction("Extract")
        extract_action.setShortcut("Ctrl+E")
        capture_action = self.menu_bar.addAction("Capture")
        capture_action.setShortcut("Ctrl+C")

        about_action = help_menu.addAction("About")
        about_action.setShortcut("Ctrl+l")

        # Setting up icons for actions
        open_icon = QIcon(open_icon_path)
        save_icon = QIcon(save_icon_path)
        extract_icon = QIcon(extract_icon_path)
        capture_icon = QIcon(capture_icon_path)
        about_icon = QIcon(about_icon_path)
        open_action.setIcon(open_icon)
        save_action.setIcon(save_icon)
        extract_action.setIcon(extract_icon)
        capture_action.setIcon(capture_icon)
        about_action.setIcon(about_icon)
        
        # Connecting actions to functions
        open_action.triggered.connect(self.select_image)
        save_action.triggered.connect(self.save_text)
        extract_action.triggered.connect(self.extract_text)
        capture_action.triggered.connect(self.open_capture_window)
        about_action.triggered.connect(self.open_about_window)

        # Setting up widgets for displaying image and text
        self.image_label = QLabel(self)
        self.btn_extract_text = QPushButton('Extract Text', self)
        self.text_edit = QTextEdit(self)
        
        self.btn_clear_text = QPushButton("Clear", self)
        self.btn_copy_text = QPushButton("Copy", self)
        
        # Connecting buttons to functions
        self.btn_extract_text.clicked.connect(self.extract_text)
        self.btn_clear_text.clicked.connect(self.clear_text)
        self.btn_copy_text.clicked.connect(self.copy_text)
        
        # Setting fixed size for buttons
        self.btn_extract_text.setFixedSize(100, 30)
        self.btn_clear_text.setFixedSize(100, 30)
        self.btn_copy_text.setFixedSize(100, 30)
        
        # Setting up layout for the widgets
        body_layout = QGridLayout()
        
        # Setting styles for image and text display widgets
        self.image_label.setStyleSheet('border: 2px solid black')
        self.image_label.setFixedSize(700, 700)
        self.text_edit.setStyleSheet('border: 2px solid black;')
        self.text_edit.setFixedSize(700, 700)
        
        # Adding widgets to the layout
        body_layout.addWidget(self.image_label, 0, 0)  
        body_layout.addWidget(self.btn_extract_text, 0, 1)  
        body_layout.addWidget(self.text_edit, 0, 2)  
        body_layout.addWidget(self.btn_clear_text, 1, 2,
            QtCore.Qt.AlignBottom)
        body_layout.addWidget(self.btn_copy_text, 1, 2,
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight) 
        body_layout.addWidget(self.progress_bar, 1, 0)  
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(body_layout)
        main_layout.setMenuBar(self.menu_bar)

        self.setLayout(main_layout)
        self.setWindowTitle("ETFT") #Extract Text From Transcript
        self.setWindowIcon(QIcon(favicon_path))
        self.setGeometry(300, 300, 1000, 700)
        self.show()

    # Add the following event handlers to the class 
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_name = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_name) 
    
    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Upload', '', 'Images (*.png *.xpm *.jpg *.bmp);;All Files (*)', options=options)
        if file_name:
            self.set_image(file_name)

    def set_image(self, file_name):
        self.image_path = file_name
        pixmap = QtGui.QPixmap(file_name)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setPixmap(pixmap)

    def open_capture_window(self):
        from view.capture_window import CaptureWindow
        self.capture_window = CaptureWindow()

    def extract_text(self):
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, 'Warning', 'Please upload an image first!')
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(100)

        from controller.text_extractor import extract_text_from_image
        text = extract_text_from_image(self.image_path, self.progress_bar)

        self.text_edit.setText(text)
        self.progress_bar.setVisible(False)
        self.btn_copy_text.setText("Copy Text")
        QMessageBox.information(self, 'Extracted Status', 'Text extracted successfully...')

    def clear_text(self):
        self.text_edit.clear()

    def copy_text(self):
        text = self.text_edit.toPlainText()
        if text:
            # Copy the text to the clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            # Show a message box to indicate that the text has been copied
            self.btn_copy_text.setText("Copied ✓")
        else:
            QMessageBox.warning(self, 'Warning', 'Nothing to copy!')

    def save_text(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Text", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            text = self.text_edit.toPlainText()
            if text:
                with open(file_name, "w", encoding='utf8') as file:
                    file.write(text)
                QMessageBox.information(self, "Save Successful", "Text saved successfully.")
            else:
                QMessageBox.warning(self, "Nothing to save", "The text area is empty.")

    def open_about_window(self):
        QMessageBox.information(self, 'Information', 'Welcome to our ETFT Application\n\n'
                                                   + 'Are you searching for a convenient and fast solution for extracting exam scores from student transcripts? Our OCR application is the solution you need.\n\n '
                                                   + 'Using OCR technology, our application helps you convert the text information on student transcripts into easily accessible and quick-to-read score formats. This saves time and effort in the process of inputting exam scores.\n\n'
                                                   + 'To use our application, all you need to do is take a picture of the student transcript using your phone or camera, then upload the image to the application. The OCR technology will automatically recognize and extract the exam score information from the transcript and display it on your screen.\n\n'
                                                   + 'With a user-friendly and easy-to-use interface, our application helps you save time and improve the efficiency of your work, especially for those who need to input exam scores for multiple students.\n\n'
                                                   + 'With our OCR application, you can easily and quickly extract exam scores from student transcripts and manage them efficiently.\n\n'
                                                   + '--\n'
                                                   + 'Author: B, N, K, T, T\n'
                                                   + 'Version: 1.0\n'
                                                   + 'The project name: "Build an App to Recognize Test Scores From Photos Capture Report Cards Using OCR Technology"' )