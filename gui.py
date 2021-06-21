import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QMessageBox, QDesktopWidget


class Application(QWidget):
    def __init__(self):
        super(Application, self).__init__()
        self.initUI()

    def initUI(self):
        # init window
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Ransomtion Protecware')
        self.resize(1000, 600)

        # centered window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.show()

        # Buttons
        self.closeButton = QPushButton(self)
        self.closeButton.setText("Close")  # text
        self.closeButton.setShortcut('Ctrl+D')  # shortcut key
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setToolTip("Close the widget")  # Tool tip
        self.closeButton.move(100, 100)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())
