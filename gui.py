import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QMessageBox, QListWidget, QGridLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Application(QWidget):
    def __init__(self):
        super(Application,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ransomtion Protecware")
        self.resize(1000, 600)
        layout = QGridLayout()
        #centered window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        #buttons
        self.closeButton = QPushButton(self)
        self.closeButton.setText("Close") #text
        self.closeButton.setShortcut('Ctrl+D')  #shortcut key
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setToolTip("Close the widget") #Tool tip
        self.closeButton.move(920,570) 

        #list
        self.listWidget = QListWidget()
        self.listWidget.resize(300, 120)
        self.listWidget.addItem("Item 1")
        self.listWidget.addItem("Item 2")
        self.listWidget.addItem("Item 3")
        self.listWidget.addItem("Item 4")
        self.listWidget.setWindowTitle('QListwidget Example')
        self.listWidget.itemClicked.connect(self.clickedList)
        layout.addWidget(self.listWidget)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def clickedList(self, item):
        QMessageBox.information(self, "ListWidget", "ListWidget: " + item.text())
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())