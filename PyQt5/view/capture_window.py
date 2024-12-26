import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QGridLayout, QWidget, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap


class CaptureWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        capture_window = QMainWindow(self)
        capture_window.setGeometry(600, 100, 700, 700)
        capture_window.setWindowTitle('ETFT - Webcam')

        # Add a label to the new window to display the captured image
        self.capture_label = QLabel(capture_window)
        #self.capture_label.setStyleSheet('border: 1px solid black')
        self.capture_label.setFixedSize(700, 700)   
    
        # Create a button for capturing the image
        capture_button = QPushButton('Capture', self)
        capture_button.setFixedSize(100, 30)
        capture_button.clicked.connect(self.take_screenshot)
        save_capture_button = QPushButton('SaveCapture', self)
        save_capture_button.setFixedSize(100, 30)
        save_capture_button.clicked.connect(self.save_capture)
        cancel_capture_button = QPushButton('Cancel', self)
        cancel_capture_button.setFixedSize(100, 30)
        cancel_capture_button.clicked.connect(self.cancel_capture)

        capture_layout = QGridLayout()
        capture_layout.addWidget(self.capture_label, 0, 0)
        capture_layout.addWidget(capture_button, 1, 0, QtCore.Qt.AlignRight)
        capture_layout.addWidget(save_capture_button, 1, 0, QtCore.Qt.AlignLeft)
        capture_layout.addWidget(cancel_capture_button, 1, 0, QtCore.Qt.AlignCenter)

        capture_widget = QWidget(self)
        capture_widget.setLayout(capture_layout)
        capture_window.setCentralWidget(capture_widget)
        capture_window.show()

        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def cancel_capture(self):
        self.timer.start()

    def take_screenshot(self):
        # Pause the timer
        self.timer.stop()

        # Display the current frame in a separate window
        ret, frame = self.cap.read()
        cv2.imshow("Drop your image", frame)
        cv2.moveWindow("Drop your image", 630, 100)

        # Allow the user to select the ROI
        roi = cv2.selectROI("Drop your image", frame, fromCenter=True, showCrosshair=True)
        cv2.destroyWindow("Drop your image")

        # Crop the frame using the ROI
        x, y, w, h = roi
        cropped_frame = frame[y:y+h, x:x+w]

        self.last_frame = cropped_frame
        return ret, cropped_frame
    
    def save_capture(self):
        frame = self.last_frame
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG (*.png);;JPEG (*.jpeg *.jpg);;BMP (*.bmp)", options=options)
        if fileName:
            if frame is None:
                print("Error capturing frame")
                return
        
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            pixmap.save(fileName)
            
    def update_frame(self):
        print("update_frame method called")
        ret, frame = self.cap.read()
        if not ret:
            print("Error capturing frame")
            self.timer.stop()
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (700, 700)) # resize the frame to 700x700
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.capture_label.setPixmap(pixmap)
