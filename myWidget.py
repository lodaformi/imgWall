# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
import time

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

    def update_image(self):
        tempList = self.imagelist.selectImg()
        print(tempList)
        # print(self.top_layout.count())
        for i in range(len(tempList)):
            self.img = tempList[i]
            widget = self.top_layout.itemAt(i).widget()
            if isinstance(widget, ImgWidget):
                widget.pixmap = QPixmap(tempList[i])
                widget.getfileName(tempList[i])
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


class ImageRecogWidget(QWidget):
    def __init__(self,parent=None):
        super(ImageRecogWidget, self).__init__(parent)
        self.font = QFont("楷体", 14, QFont.Bold)

        inputLabel = QLabel("照片导入")
        inputLabel.setFont(self.font)

        openSiteLabel = QLabel("打开位置")
        openSiteLabel.setFont(self.font)

        self.openSite = QLineEdit()

        openButton = QPushButton()
        openButton.setIcon(QIcon(QPixmap("img/folder0.jpg")))

        searchButton = QPushButton("查询")
        searchButton.setIcon(QIcon("img/query.jpg"))

        objectLabel = QLabel("物体识别")
        objectLabel.setFont(self.font)

        self.resultLabel = QLabel()
        self.resultLabel.setFont(QFont("Roman times", 16))
        self.infoLabel = QLabel()
        self.infoLabel.setFont(QFont("Roman times", 16))
        self.infoWiget = QWidget()
        self.infoWigLayout = QGridLayout()
        self.infoWiget.setLayout(self.infoWigLayout)
        self.infoWigLayout.addWidget(self.infoLabel,0,0)
        self.infoWigLayout.addWidget(self.resultLabel,1,0)


        imageLayout = QGridLayout()
        imageLayout.addWidget(inputLabel,0,0,1,4,Qt.AlignCenter)
        imageLayout.addWidget(openSiteLabel,1,0)
        imageLayout.addWidget(self.openSite,1,1)
        imageLayout.addWidget(openButton,1,2)
        imageLayout.addWidget(searchButton,1,3)

        self.downLayout = QGridLayout()
        self.downLayout.setSpacing(20)

        self.downLayout.addLayout(imageLayout,0,0)

        self.downLayout.addWidget(objectLabel,0,1, Qt.AlignCenter)
        self.downLayout.addWidget(self.infoWiget,1,1, Qt.AlignCenter)
        self.downLayout.setRowStretch(0, 1)
        self.downLayout.setRowStretch(1, 8)
        self.downLayout.setColumnStretch(0, 3)
        self.downLayout.setColumnStretch(1, 1)

        self.setLayout(self.downLayout)

        self.picWidget = QWidget()
        self.picLayout = QHBoxLayout()
        self.picWidget.setLayout(self.picLayout)
        self.downLayout.addWidget(self.picWidget,1,0)

        openButton.clicked.connect(self.openPicture)
        searchButton.clicked.connect(self.search)

    def updateText(self, text):
        print('update text：{}'.format(text))
        self.infoLabel.setText(text)

    def cleanPic(self):
        if self.picWidget.layout():
            layout = self.picWidget.layout()
            # print(layout.count())
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if isinstance(item, QWidgetItem):
                    item.widget().close()
                layout.removeItem(item)

            QWidget().setLayout(self.picWidget.layout())
            self.picLayout = QHBoxLayout()
            self.picWidget.setLayout(self.picLayout)

    def openPicture(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', './')
        if self.filename[0]:
            self.openSite.setText(self.filename[0])
            self.cleanPic()
            self.cameraWidget = ImgWidget(400, 300)
            self.cameraWidget.pixmap = QPixmap(self.filename[0])
            self.cameraWidget.updatePixmap()
            # self.cameraWidget = VideoWidget(self.filename[0],400, 300)
            self.picLayout.addWidget(self.cameraWidget)
            self.picWidget.show()
        # # self.repaint()
        # print(self.updatesEnabled())
        # time.sleep(1)
        # print('update')
        # time.sleep(5)
        # print('done')

    def search(self):
        files = self.filename[0]
        thread = MyThread(files, self)
        thread.start_trigger.connect(self.updateText)
        thread.end_trigger.connect(self.updateText)
        thread.start()


# class MyThread2(QThread):
#     start_trigger = pyqtSignal(str)
#     end_trigger = pyqtSignal(str)
#
#     def __init__(self, files, parent=None):
#         super(MyThread2, self).__init__(parent)
#         self.file = files
#
#     def run(self):
#         print('sleep ..')
#         self.start_trigger.emit('start ...')
#         startTime = time.time()
#         find_img(self.file)
#         os.system('rm -fr {}/diary'.format(file_path))
#         os.system('cd {} && matlab -nodesktop -nosplash -nojvm -r "testPascalVocPic;quit;"'.format(file_path))
#         os.system('grep -A20 Elapsed {}/diary | tail -n +2 > {}/result.txt'.format(file_path,file_path))
#         totalTime = time.time() - startTime
#
#         resultFile = open('{}/result.txt'.format(file_path),'r')
#         string_result = ""
#         for line in resultFile:
#             list = line.split()
#             obj = list[0]
#             score = list[1]
#             # print(score)
#             if float(score) > 0:
#                 string_result = string_result + '\n' + obj
#         resultFile.close()
#
#         self.end_trigger.emit('end...')
#         time.sleep(0.5)
#         # self.end_trigger.emit(string_result)
#         self.end_trigger.emit( string_result + '\n\n' + "total time: {:.2f}s".format(totalTime))

class PageButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(PageButton, self).__init__(*args, **kwargs)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('QPushButton {border: none;}'
                           'QPushButton:hover { color: #3498DB; '
                           'text-decoration: underline; }')