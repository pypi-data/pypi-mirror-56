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

class Scene(QGraphicsScene):
    NameItem = 1
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.addText("Hello, world!")
        self.counterItems=0
        self.selectedIndex=0
        self.paintPointer=QGraphicsEllipseItem()
        self.paintPointer.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.paintPointer.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.addItem(self.paintPointer)



    def addNewPixmap(self,picture):
        self.item=QGraphicsPixmapItem(picture)
        self.item.setTransformationMode(Qt.SmoothTransformation)
        self.addItem(self.item)



    def addNewItem(self,counterItems,item):

        self.counterItems=counterItems
        item.setData(Scene.NameItem,self.counterItems)
        self.addItem(item)

        ellipseItem_1=QGraphicsEllipseItem()
        ellipseItem_2=QGraphicsEllipseItem()
        ellipseItem_3=QGraphicsEllipseItem()
        ellipseItem_4=QGraphicsEllipseItem()
        ellipsRadius=10
        ellipseItem_1.setRect(item.rect().x()-ellipsRadius/2,item.rect().y()-ellipsRadius/2,ellipsRadius,ellipsRadius)
        ellipseItem_2.setRect(item.rect().x()+item.rect().width()-ellipsRadius/2,item.rect().y()-ellipsRadius/2,ellipsRadius,ellipsRadius)
        ellipseItem_3.setRect(item.rect().x()-ellipsRadius/2,item.rect().y()+item.rect().height()-ellipsRadius/2,ellipsRadius,ellipsRadius)
        ellipseItem_4.setRect(item.rect().x()+item.rect().width()-ellipsRadius/2,item.rect().y()+item.rect().height()-ellipsRadius/2,ellipsRadius,ellipsRadius)

        ellipsItemsList=[ellipseItem_1,ellipseItem_2,ellipseItem_3,ellipseItem_4]
        for item in ellipsItemsList:
            item.setBrush(QBrush(QtCore.Qt.yellow, style = QtCore.Qt.BDiagPattern))
            item.setData(Scene.NameItem,self.counterItems)
            self.addItem(item)
