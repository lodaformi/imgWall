from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class VideoWidget(QWidget):
    # def __init__(self, length, width, parent=None):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # self.default_pixmap = QPixmap(picture)
        self.default_pixmap = QPixmap('./images/horse.jpg')
        self.pixmap = None
        self.imageLabel = QLabel()
        layout = QHBoxLayout()
        layout.addWidget(self.imageLabel)
        # print(self.default_pixmap.isNull())
        self.imageLabel.setMinimumSize(600,300)
        # self.imageLabel.setMaximumSize(200,200)
        self.imageLabel.setPixmap(self.default_pixmap)
        self.setLayout(layout)
        self.center()
        # self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
        #                    QtGui.QSizePolicy.MinimumExpanding,)

    def resizeEvent(self, event):
        self.updatePixmap()

    def updatePixmap(self):
        if self.pixmap:
            show_pixmap = self.pixmap.copy()
        else:
            show_pixmap = self.default_pixmap.copy()
        # print(self.imageLabel.height())
        show_pixmap = show_pixmap.scaledToWidth(
            # self.imageLabel.height(),
            self.imageLabel.width(),
            Qt.SmoothTransformation)
        # print(self.imageLabel.width())
        self.imageLabel.setPixmap(show_pixmap)

    def paintEvent(self, event):
        pass

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    vw = VideoWidget()
    vw.pixmap = QPixmap('./images/train.jpg')
    vw.updatePixmap()
    vw.show()
    sys.exit(app.exec_())
