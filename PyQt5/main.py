import sys
import os
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    app.setStyleSheet(open("style.qss", "r").read())
    ex = MainWindow()
    ex.setGeometry(200, 50, 1500, 800)
    sys.exit(app.exec_())