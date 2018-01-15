# -*- coding: utf-8 -*-
# from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class ObjectDetectionInterface(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        self.resize(901, 650)

        centralwidget = QWidget(self)
        self.pushButton = QPushButton(centralwidget)
        self.pushButton.setGeometry(QRect(110, 50, 93, 52))
        font = Font()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.setText(_translate("MainWindow", "实时识别", None))



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    odi = ObjectDetectionInterface()
    odi.show()
    sys.exit(app.exec_())