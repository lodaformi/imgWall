# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
import time
import random
from copy import deepcopy

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from randomImage import imgList

class ImgWidget(QWidget):
    #define signal
    mysignal = pyqtSignal(QPixmap, str)

    def __init__(self, parent=None, connect_fun=None):
        QWidget.__init__(self, parent)
        self.default_pixmap = QPixmap('./images/blank.png')
        self.pixmap = None
        self.filename = ''
        self.imageLabel = QLabel()
        self.imageLabel.setMaximumSize(QSize(360,360))
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.imageLabel)
        # print(self.default_pixmap.isNull())
        # self.imageLabel.setMinimumSize(200,200)
        self.setContentsMargins(0, 0, 0, 0)
        self.imageLabel.setPixmap(self.default_pixmap)
        self.setLayout(layout)

        # self.setStyleSheet('''
        # border: 1px solid black
        # ''')
        # self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
        #                    QtGui.QSizePolicy.MinimumExpanding,)

        if connect_fun:
            self.mysignal.connect(connect_fun)

    def getfileName(self, filename):
        self.filename = filename

    def run(self):
        self.mysignal.emit(self.pixmap, self.filename)
        # time.sleep(1)

    def get(self, pixObj):
        print(pixObj)
        # self.pixmap = pixObj

    def resizeEvent(self, event):
        self.updatePixmap()

    def updatePixmap(self, qpixmap=None):
        if qpixmap is not None:
            self.pixmap = qpixmap

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
        # print(filename)

    def paintEvent(self, event):
        pass

    def mousePressEvent(self, QMouseEvent):
        # print('hello !')
        self.run()

class imgWall(QWidget):
    def __init__(self, parent=None, funshow=None):
        super(imgWall,self).__init__(parent)
        self.funshow = funshow
        self.imagelist = imgList()

        self.top_layout = QGridLayout()
        self.setLayout(self.top_layout)

        #generate pos list with 20*20
        #[(0,0) (0,1) ..... (0,19)
        #...
        #(19,0) (19,1) ..... (19,19)]
        self.pos = [(i,j) for i in range(20) for j in range(20) ]

        j = 0
        for i in range(len(self.pos)):
            tmp_imgWidget = ImgWidget(connect_fun=self.funshow)
            # tmp_imgWidget = ImgWidget(connect_fun=self.imgshow.updatePixmap)
            tmp_imgWidget.setVisible(False)
            self.top_layout.addWidget(tmp_imgWidget, self.pos[j][0], self.pos[j][1])
            j = j + 1

    def cleanLayout(self):
        if self.layout():
            layout = self.layout()
            # print(layout.count())
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if isinstance(item, QWidgetItem):
                    item.widget().close()
                layout.removeItem(item)

            QWidget().setLayout(self.layout())
            self.top_layout = QHBoxLayout()
            self.setLayout(self.top_layout)

    def hideWidget(self):
        if self.layout():
            layout = self.layout()
            # print(layout.count())
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if isinstance(item, QWidgetItem):
                    item.widget().hide()

    def update_image(self, fileList):
        copyList = deepcopy(fileList)
        showlist = []

        for i in range(400):
            index = random.randint(0, (len(copyList)-1))
            img_name = copyList.pop(index)
            showlist.append(img_name)

        for i in range(len(showlist)):
            widget = self.top_layout.itemAt(i).widget()
            if isinstance(widget, ImgWidget):
                widget.pixmap = QPixmap(showlist[i])
                widget.getfileName(showlist[i])
                widget.updatePixmap()
                widget.setVisible(True)

class MyThread(QThread):
    start_trigger = pyqtSignal()
    end_trigger = pyqtSignal(str)

    def __init__(self, files, modtype, modfile, parent=None):
        super(MyThread, self).__init__(parent)
        self.file = files
        self.modtype = modtype
        self.modfile = modfile

    def run(self):
        print('sleep ..')
        print(self.file)
        print(self.modfile)
        self.start_trigger.emit()
        startTime = time.time()
        #Using program replace sleep
        time.sleep(1)
        totalTime = time.time() - startTime
        # resultFile = open('/home/pdl/display/labels.txt')
        # aList = resultFile.read().split()
        #
        # string_result = ""
        # count = 0
        # for data in aList:
        #     string_result = string_result + "\n" + data
        #     count += 1
        #     if count == 3:
        #         break
        # resultFile.close()
        # self.modType = self.judgeMod()
        result_str = '{}模型分类结果:'.format(self.modtype)
        result_str += "\nTop1 类型:{} 概率:{}".format('plane', 4.3)

        self.end_trigger.emit("total time: {:.2f}s".format(totalTime) + '\n' + result_str)

class PageButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(PageButton, self).__init__(*args, **kwargs)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('QPushButton {border: none;}'
                           'QPushButton:hover { color: #3498DB; '
                           'text-decoration: underline; }')