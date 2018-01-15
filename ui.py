# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import time
import traceback
import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from myWidget import ImgWidget, imgWall , MyThread

class TopButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(TopButton, self).__init__(*args, **kwargs)
        self.setMinimumSize(20, 40)
        self.setDefault(True)
        self.setFont(QFont("楷体",14, QFont.Bold))

class userInterface(QWidget):
    def __init__(self, parent=None):
        super(userInterface, self).__init__(parent)
        self.font = QFont("楷体", 12, QFont.Bold)

        self.setWindowTitle("imageWall")
        self.setMinimumSize(1500,1000)
        self.center()

        self.imageButton = TopButton("图片墙")
        self.openButton = TopButton("选择文件夹")
        self.selectMod = TopButton("选择模型")

        self.layout = QGridLayout()
        self.layout.addWidget(self.openButton, 1, 2, 1, 1)
        self.layout.addWidget(self.selectMod, 1, 4, 1, 1)
        self.layout.addWidget(self.imageButton, 1, 6, 1, 1)

        self.setLayout(self.layout)

        self.selectLabel = QLabel("        所选分类目标")
        self.selectLabel.setFont(self.font)

        # select image widget
        self.selectImg = ImgWidget()
        self.selectImg.setMaximumSize(QSize(360, 360))
        # self.selectImg.updatePixmap()

        # imageWall
        self.imgWallWidget = imgWall(funshow=self.updateResult)
        self.layout.addWidget(self.imgWallWidget, 0, 0, 1, 8)

        #
        self.downWidget = QWidget()
        self.downlayout = QVBoxLayout()
        self.downlayout.addWidget(self.selectImg)
        self.downlayout.addWidget(self.selectLabel)

        self.downWidget.setLayout(self.downlayout)

        #result widget
        self.resultText = QLabel()
        self.resultText.setFont(self.font)

        self.resultWidget = QWidget()

        self.resultLayout = QVBoxLayout()
        self.resultWidget.setLayout(self.resultLayout)
        self.resultLayout.addWidget(self.downWidget)
        # self.resultLayout.addWidget(self.selectLabel,1 ,0)
        self.resultLayout.addWidget(self.resultText)

        self.resultWidget.setVisible(False)

        self.layout.addWidget(self.resultWidget, 0, 8, 1, 2)
        # self.layout.setColumnStretch(0, 5)
        # self.layout.setColumnStretch(1, 1)

        self.openButton.clicked.connect(self.openDir)
        self.imageButton.clicked.connect(self.loadImage)
        self.selectMod.clicked.connect(self.module)

        self.modFile = ''
        self.modType = False
        self.fileList = []

    def openDir(self):
        getfileList, _ = QFileDialog.getOpenFileNames(self, 'Open file', './')
        if not getfileList:
            return
        if len(getfileList) < 400:
            QMessageBox.information(self, 'Warnning', '选择文件数量需大于等于400！')
            return
        self.fileList = getfileList
        print(self.fileList)
        print(len(self.fileList))

    def updateResult(self, pixmap, filename):
        self.selectImg.pixmap = pixmap
        self.selectImg.updatePixmap()
        # print(filename)
        thread = MyThread(filename, self.modType, self.modFile, self)
        thread.start_trigger.connect(self.startCompute)
        thread.end_trigger.connect(self.updateInfo)
        thread.start()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def updateWidget(self):
        self.resultWidget.setVisible(True)

    def startCompute(self):
        self.resultText.setText("正在计算...")

    def updateInfo(self, info):
        self.resultText.setText("{}".format(info))

    # def cleanLayout(self):
    #     if self.downWidget.layout():
    #         layout = self.downWidget.layout()
    #         # print(layout.count())
    #         for i in reversed(range(layout.count())):
    #             item = layout.itemAt(i)
    #             if isinstance(item, QWidgetItem):
    #                 item.widget().close()
    #             layout.removeItem(item)
    #
    #         QWidget().setLayout(self.downWidget.layout())
    #         self.downLayout = QHBoxLayout()
    #         self.downWidget.setLayout(self.downLayout)

    def loadImage(self):
        if not self.fileList:
            QMessageBox.information(self, 'Warnning', '请先导入照片！')
            return
        if self.modFile == '':
            QMessageBox.information(self, 'Warnning', '请先导入模型！')
            return
        self.updateWidget()
        self.imgWallWidget.hideWidget()
        self.imgWallWidget.update_image(self.fileList)
        print("self.fileList {}".format(self.fileList))
        print(len(self.fileList))

    def module(self):
        getFile, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        if getFile == '':
            return
        else:
            print(getFile)
            if 'Vgg16' in getFile:
                self.modType = 'Vgg16'
                self.modFile = getFile
            elif 'Vgg19' in getFile:
                self.modType = 'Vgg19'
                self.modFile = getFile
            elif 'ResNet' in getFile:
                self.modType = 'ResNet'
                self.modFile = getFile
            else:
                QMessageBox.information(self, 'module type error', '请导入正确模型！')
                print(self.modType)
                return

            # print(self.modType)

    def excepthook(excType, excValue, tracebackobj):
        """
        Global function to catch unhandled exceptions.
        @param excType exception type
        @param excValue exception value
        @param tracebackobj traceback object
        """
        separator = '-' * 80
        logFile = os.path.join("simple.log")
        notice = \
            """An unhandled exception occurred. Please report the problem\n"""\
            """using the error reporting dialog or via email to <%s>.\n"""\
            """A log has been written to "%s".\n\nError information:\n""" % \
            ("yourmail at server.com", logFile)
        versionInfo = "0.0.1"
        timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

        tbinfofile = StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg = '%s: \n%s' % (str(excType), str(excValue))
        sections = [separator, timeString, separator, errmsg, separator, tbinfo]
        msg = '\n'.join(sections)
        try:
            with open(logFile, "w") as f:
                f.write(msg)
                f.write(versionInfo)
        except IOError:
            pass
        errorbox = QMessageBox()
        errorbox.setText(str(notice)+str(msg)+str(versionInfo))
        errorbox.setWindowTitle(' An Unhandled Exception Occurred')
        errorbox.exec_()

    sys.excepthook = excepthook

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = userInterface()
    ui.show()
    sys.exit(app.exec_())