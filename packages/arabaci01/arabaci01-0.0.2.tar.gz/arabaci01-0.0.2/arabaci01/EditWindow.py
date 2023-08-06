# coding=utf-8
import sys
import os

from PySide2 import QtCore, QtGui,QtWidgets
from PySide2.QtCore import Qt, Slot, Signal, QObject, QDir, QRectF, QPointF,QPoint
from PySide2.QtWidgets import*
from PySide2.QtGui import*
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (QGraphicsView,QGraphicsScene, QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,QVBoxLayout, QWidget)
from PySide2.QtCharts import QtCharts

class EditWindow(QDialog):
    updateIdSignal = Signal(int,int)
    cancelCreatingRectSignal = Signal()
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("editWindow")
        self.itemSelected=False
        self.lastChoosenIdExist=False
        self.rectCreated=False
        self.errorMessage=QErrorMessage()

        self.label = QLabel(" ")
        self.cancelButton=QPushButton("Cancel")
        self.cancelButton.setShortcut("ESC")
        self.okButton=QPushButton("OK")
        self.listWidget=QListWidget()


        self.layout = QGridLayout()
        self.layout.addWidget(self.label,0,0)
        self.layout.addWidget(self.cancelButton,1,0)
        self.layout.addWidget(self.okButton,1,1)
        self.layout.addWidget(self.listWidget,2,0, 2,2)
        self.setLayout(self.layout)
        self.setTabOrder(self.okButton, self.cancelButton)

        self.listWidget.currentRowChanged.connect(self.listWidgetRowChaged)
        self.listWidget.itemDoubleClicked.connect(self.listWidgetDoubleClicked)
        self.okButton.clicked.connect(self.okButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

    @Slot()
    def setLastChoosenId(self,lastChoosenId):
        self.lastChoosenId=lastChoosenId
        self.lastChoosenIdExist=True
        self.listWidget.setCurrentRow(self.lastChoosenId)


    @Slot()
    def listWidgetRowChaged(self):
        if (self.listItems[self.listWidget.currentRow()][-1]=="\n"):
            self.label.setText(self.listItems[self.listWidget.currentRow()][:-1])
        else:
            self.label.setText(self.listItems[self.listWidget.currentRow()])
        self.itemSelected=True

    @Slot()
    def listWidgetDoubleClicked(self,item):
        self.itemSelected=True
        self.updateIdSignal.emit(self.listWidget.row(item),self.rectCreated)
        self.rectCreated=False
        self.close()

    @Slot()
    def okButtonClicked(self,clicked):
        if (self.itemSelected==True):
            self.updateIdSignal.emit(self.listWidget.currentRow(),self.rectCreated)
            self.rectCreated=False
            self.close()
        else:
            self.errorMessage.showMessage("Choose a class")

    @Slot()
    def cancelButtonClicked(self,clicked):
        self.cancelCreatingRectSignal.emit()
        self.close()


    def readClassesTxt(self,dirName):
        self.dirName=dirName
        list=self.dirName.split("/")
        list.append("classes.txt")
        path="/".join(list)
        if (os.path.isfile(path)):
            f=open(path, "r")
            content=f.readlines()
            f.close()
            self.listItems=content
            if (self.listItems):
                for className in self.listItems:
                    item=QtWidgets.QListWidgetItem()
                    if (className[-1]=="\n"):
                        item.setText(className[:-1])  #removed "/n"
                    else:
                        item.setText(className)  #removed "/n"

                    self.listWidget.addItem(item)
        else:
            self.errorMessage.showMessage("classes.txt does not exist")
            self.close()
