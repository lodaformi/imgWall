from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from randomImage import imgList

class ImgWidget(QWidget):
    #define signal
    mysignal = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # self.default_pixmap = QPixmap(picture)
        self.default_pixmap = QPixmap('./images/train.jpg')
        self.pixmap = None
        self.imageLabel = QLabel()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.imageLabel)
        # print(self.default_pixmap.isNull())
        # self.imageLabel.setMinimumSize(200,200)
        self.setContentsMargins(0, 0, 0, 0)
        self.imageLabel.setPixmap(self.default_pixmap)
        self.setLayout(layout)

        self.mysignal.connect(self.get)
        # self.setStyleSheet('''
        # border: 1px solid black
        # ''')
        # self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
        #                    QtGui.QSizePolicy.MinimumExpanding,)

    def run(self):
        self.mysignal.emit(self.pixmap)

    def get(self, pixObj):
        print(pixObj)
        # self.pixmap = pixObj

    def resizeEvent(self, event):
        self.updatePixmap()

    def updatePixmap(self):
        if self.pixmap:
            show_pixmap = self.pixmap.copy()
        else:
            show_pixmap = self.default_pixmap.copy()
        # print(self.imageLabel.height())
        show_pixmap = show_pixmap.scaledToWidth(
            # self.imageLabel.width(),
            self.width(),
            Qt.SmoothTransformation)
        # print(self.imageLabel.width())
        self.imageLabel.setPixmap(show_pixmap)

    def paintEvent(self, event):
        pass

    def mousePressEvent(self, QMouseEvent):
        # print('hello !')
        # print(self.pixmap)
        self.run(self.pixmap)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    iw = ImgWidget()
    iw.pixmap = QPixmap('./images/horse.jpg')
    iw.show()
    sys.exit(app.exec_())