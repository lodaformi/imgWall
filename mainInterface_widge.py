# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from  myWidget import ImageRecogWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TopButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(TopButton, self).__init__(*args, **kwargs)
        self.setMinimumSize(20, 40)
        self.setDefault(True)
        self.setFont(QFont("楷体",14, QFont.Bold))

class ObjectDetectionInterface(QWidget):
    def __init__(self, parent=None):
        super(ObjectDetectionInterface, self).__init__(parent)
        self.setWindowTitle("object detection")
        self.setMinimumSize(1000,850)

        self.realTimeWidget = RealTimeWidget()
        self.imageRecogWidget = ImageRecogWidget()
        self.imageRecogWidget2 = ImageRecogWidget2()
        # self.tagSearchWidget = TagSearchWidget()
        self.mapGraphWidget = MapGraphWidget()

        self.realTimeButton = TopButton("实时识别")
        #print(self.realTimeWidget)
        self.imageRecogButton = TopButton("图片识别")
        self.imageRecogButton2 = TopButton("图片识别2")
        self.tagSearchButton = TopButton("标签搜索")
        self.mapGraphButton = TopButton("以图搜图")

        self.layout = QGridLayout()
        self.layout.setSpacing(30)
        # self.layout.setMargin(50)

        self.layout.addWidget(self.realTimeButton,0,0)
        self.layout.addWidget(self.imageRecogButton,0,1)
        self.layout.addWidget(self.imageRecogButton2,0,2)
        # self.layout.addWidget(self.tagSearchButton,0,2)
        self.layout.addWidget(self.mapGraphButton,0,3)

        self.setLayout(self.layout)

        self.downWidget = QWidget()
        self.layout.addWidget(self.downWidget,1,0,1,4)

        self.downLayout = QHBoxLayout()
        self.downWidget.setLayout(self.downLayout)

        self.realTimeButton.clicked.connect(self.realTime)
        self.imageRecogButton.clicked.connect(self.imageRecog)
        self.imageRecogButton2.clicked.connect(self.imageRecog2)
        # self.tagSearchButton.clicked.connect(self.tagSearch)
        self.mapGraphButton.clicked.connect(self.mapSearch)

    def cleanLayout(self):
        if self.downWidget.layout():
            layout = self.downWidget.layout()
            # print(layout.count())
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if isinstance(item, QWidgetItem):
                    item.widget().close()
                layout.removeItem(item)

            QWidget().setLayout(self.downWidget.layout())
            self.realTimeWidget.cameraWidget.off()
            self.downLayout = QHBoxLayout()
            self.downWidget.setLayout(self.downLayout)

    # def realTime(self):
    #     self.cleanLayout()
    #     self.realTimeWidget.cameraWidget.on()
    #     # print(self.realTimeWidget)
    #     self.downWidget.layout().addWidget(self.realTimeWidget)
    #     self.realTimeWidget.show()
    #
    # def imageRecog(self):
    #     self.cleanLayout()
    #     self.downWidget.layout().addWidget(self.imageRecogWidget)
    #     self.imageRecogWidget.show()
    #
    # def imageRecog2(self):
    #     self.cleanLayout()
    #     self.downWidget.layout().addWidget(self.imageRecogWidget2)
    #     self.imageRecogWidget2.show()
    #
    # # def tagSearch(self):
    # #     self.cleanLayout()
    # #     self.downWidget.layout().addWidget(self.tagSearchWidget)
    # #     self.tagSearchWidget.show()

    def mapSearch(self):
        self.cleanLayout()
        self.downWidget.layout().addWidget(self.mapGraphWidget)
        self.mapGraphWidget.show()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    odi = ObjectDetectionInterface()
    odi.show()
    sys.exit(app.exec_())