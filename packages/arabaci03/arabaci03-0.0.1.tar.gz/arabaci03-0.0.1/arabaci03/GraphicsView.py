import sys
import os

from PySide2 import QtCore, QtGui,QtWidgets
from PySide2.QtCore import Qt, Slot, Signal, QObject, QDir, QRectF, QPointF,QPoint
from PySide2.QtWidgets import*
from PySide2.QtGui import*
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (QGraphicsView,QGraphicsScene, QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,QVBoxLayout, QWidget)
from PySide2.QtCharts import QtCharts

class GraphicsView(QGraphicsView):
    createdRectPositionSignal=Signal(int,int,int,int)
    movedRectPositionSignal=Signal(int,int,int,int)
    resizedRectPositionalSignal=Signal(int,int,int,int)
    itemSelectionChangedSignal = Signal(int)
    paintRectSignal = Signal(int, int)
    enableIdInputOfCreatedRectSignal=Signal()
    mousePressedOnNoItemSignal=Signal()
    jumpToCreateRectAppSinal=Signal(bool)
    setUpWindowSignal=Signal()
    def __init__(self,scene):
        QGraphicsView.__init__(self)

        #Graphics
        self.scene=scene
        self.alignment = Qt.Alignment(Qt.AlignVCenter, Qt.AlignHCenter)
        self.setAlignment(self.alignment)
        self.itemSelected=False
        self.mousePressedForRect=False
        self.mousePressedForPainting=False
        self.rectItemPressed=False
        self.ellipseItemPressed=False
        self.mouseMovedForDrawing=False
        self.mousePressedForCreatingTemplate=False
        self.paintEventEnabled=False
        self.createTemplateEventEnabled=False
        self.drawRect=False
        self.advancedMode=False
        self.rectMoved=False
        self.rectResized=False
        self.listOfItems=[]
        self.pos1 = [0,0]
        self.pos2 = [0,0]
        self.viewWidth=0
        self.viewHeight=0
        self.widthMargin=0
        self.heightMargin=0
        self.zoomOutFactor=1
        self.zoomInFactor=1
        self.netZoomFactor=1
        self.netDeltaX=0
        self.totalDelta=QPointF(0,0)
        self.delta=0
        self.ellipseRadius=10
        self.paintingEnabled=False
        self.createTemplateEnabled=False
        self.paintingColor=QColor()
        self.setRenderHints(QPainter.Antialiasing
                | QPainter.SmoothPixmapTransform
                | QPainter.TextAntialiasing)

    @Slot()
    def painterSizeSlot(self, size, red,green,blue,alpha):
        print ("painterSizeSlot")
        self.setUpWindowSignal.emit()
        self.scale(self.netZoomFactor, self.netZoomFactor)
        self.viewSettingsChanged()
        self.paintingColor.setRedF(red)
        self.paintingColor.setGreenF(green)
        self.paintingColor.setBlueF(blue)
        self.paintingColor.setAlphaF(alpha)
        self.painterSize=size
        self.listOfItems=self.items()
        for item in self.listOfItems:
            if (isinstance(item,  QGraphicsEllipseItem)&((-1)==item.data(self.scene.NameItem))):
                self.pointerItem=item
        self.paintingEnabled=True

    @Slot()
    def painterSizeTempSlot(self, size,red,green,blue,alpha):
        print ("painterSizeTempSlot")
        self.setUpWindowSignal.emit()
        self.scale(self.netZoomFactor, self.netZoomFactor)
        self.viewSettingsChanged()
        self.painterSize=size
        self.paintingColor.setRedF(red)
        self.paintingColor.setGreenF(green)
        self.paintingColor.setBlueF(blue)
        self.paintingColor.setAlphaF(alpha)
        self.listOfItems=self.items()
        for item in self.listOfItems:
            if (isinstance(item,  QGraphicsEllipseItem)&((-1)==item.data(self.scene.NameItem))):
                self.pointerItem=item
        self.createTemplateEnabled=True

    def wheelEvent(self, event):
        # Zoom Factor
        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor


        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.delta() > 0:
            self.zoomFactor = self.zoomInFactor
            self.netZoomFactor = self.netZoomFactor*self.zoomInFactor
        else:
            self.zoomFactor = self.zoomOutFactor
            self.netZoomFactor = self.netZoomFactor/self.zoomInFactor
        self.scale(self.zoomFactor, self.zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        self.delta = newPos - oldPos
        self.totalDelta+=self.delta
        self.translate(self.delta.x(), self.delta.y())

     #   self.setUpWindowSignal.emit()
     #   self.scale(self.netZoomFactor, self.netZoomFactor)
    #    self.translate(self.delta.x(), self.delta.y())
        self.viewSettingsChanged()

    def viewSettingsChanged(self):
        self.sceneWidth=self.sceneRect().width()
        self.sceneHeight=self.sceneRect().height()
        if (self.viewWidth/self.sceneWidth)>(self.viewHeight/self.sceneHeight):
            self.graphScale=(self.viewHeight/self.sceneHeight)*self.netZoomFactor
            self.heightMargin=(self.viewHeight-(self.sceneHeight*self.graphScale))/2
            self.widthMargin=(self.viewWidth-(self.sceneWidth*self.graphScale))/2
        else:
            self.graphScale=(self.viewWidth/self.sceneWidth)*self.netZoomFactor
            self.widthMargin=(self.viewWidth-(self.sceneWidth*self.graphScale))/2
            self.heightMargin=(self.viewHeight-(self.sceneHeight*self.graphScale))/2

    @Slot()
    def checkListWidgetRowChanged(self,currentRow):
        self.selectedIndex=currentRow
        self.itemSelected=True
        self.listOfItems=self.items()
        for item in self.listOfItems:
            if (isinstance(item, QGraphicsRectItem)&(self.selectedIndex==item.data(self.scene.NameItem))):
                item.setBrush(QBrush(QtCore.Qt.yellow, style = QtCore.Qt.BDiagPattern))
                item.setOpacity(0.15)
                self.itemSelected==True
              #  if (self.drawRect==False):
                   # self.itemSelectionChangedSignal.emit(self.selectedIndex)

            elif (isinstance(item, QGraphicsRectItem)&(self.selectedIndex!=item.data(self.scene.NameItem))):
                item.setBrush(QBrush(QtCore.Qt.transparent, style = QtCore.Qt.BDiagPattern))
    @Slot()
    def keyPressEvent(self, event):
        if (self.itemSelected==True):
            self.tempSelectedIndex=self.selectedIndex
            for item in self.listOfItems:
                if (isinstance(item, QGraphicsRectItem)&(self.tempSelectedIndex==item.data(self.scene.NameItem))):
                    self.selectedItem=item
            self.itemAtZero_x=self.selectedItem.rect().x()
            self.itemAtZero_y=self.selectedItem.rect().y()
            self.itemAtZero_width=self.selectedItem.rect().width()
            self.itemAtZero_height=self.selectedItem.rect().height()
            self.changeOnY=0
            self.changeOnX=0

            if event.key() == QtCore.Qt.Key_Up:
                self.changeOnY=self.changeOnY-5
            elif event.key() == QtCore.Qt.Key_Down:
                self.changeOnY=self.changeOnY+5
            elif event.key() == QtCore.Qt.Key_Left:
                self.changeOnX=self.changeOnX-5
            elif event.key() == QtCore.Qt.Key_Right:
                self.changeOnX=self.changeOnX+5
            for item in self.listOfItems:
                if (isinstance(item, QGraphicsRectItem)&(self.tempSelectedIndex==item.data(self.scene.NameItem))):
                    self.itemToBeMoved=item

            self.scaledchangeOnX=float(self.changeOnX)/self.graphScale
            self.scaledchangeOnY=float(self.changeOnY)/self.graphScale
            if(((self.itemAtZero_x+self.scaledchangeOnX)>0)&((self.itemAtZero_y+self.scaledchangeOnY)>0)&((self.itemAtZero_x+self.scaledchangeOnX+self.itemAtZero_width)<(self.sceneWidth))&((self.itemAtZero_y+self.scaledchangeOnY+self.itemAtZero_height)<(self.sceneHeight))):
                self.itemToBeMoved.setRect((self.itemAtZero_x+self.scaledchangeOnX), (self.itemAtZero_y+self.scaledchangeOnY), self.itemAtZero_width, self.itemAtZero_height)
                listOfLinkedEllipseItems=[]
                for item in self.listOfItems:
                    if (isinstance(item, QGraphicsEllipseItem)&(self.selectedIndex==item.data(self.scene.NameItem))):
                        listOfLinkedEllipseItems.append(item)

                listOfLinkedEllipseItems[0].setRect(self.itemToBeMoved.rect().x()-self.ellipseRadius/2,self.itemToBeMoved.rect().y()-self.ellipseRadius/2,self.ellipseRadius,self.ellipseRadius)
                listOfLinkedEllipseItems[1].setRect(self.itemToBeMoved.rect().x()+self.itemToBeMoved.rect().width()-self.ellipseRadius/2,self.itemToBeMoved.rect().y()-self.ellipseRadius/2,self.ellipseRadius,self.ellipseRadius)
                listOfLinkedEllipseItems[2].setRect(self.itemToBeMoved.rect().x()-self.ellipseRadius/2,self.itemToBeMoved.rect().y()+self.itemToBeMoved.rect().height()-self.ellipseRadius/2,self.ellipseRadius,self.ellipseRadius)
                listOfLinkedEllipseItems[3].setRect(self.itemToBeMoved.rect().x()+self.itemToBeMoved.rect().width()-self.ellipseRadius/2,self.itemToBeMoved.rect().y()+self.itemToBeMoved.rect().height()-self.ellipseRadius/2,self.ellipseRadius,self.ellipseRadius)
                self.movedRectPositionSignal.emit((self.itemToBeMoved.rect().x()), (self.itemToBeMoved.rect().y()), self.itemToBeMoved.rect().width(), self.itemToBeMoved.rect().height())

            event.accept()

    @Slot()
    def mousePressEvent(self, event):
        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()
        self.paintPos = self.mapToScene(event.pos())
        if(((self.widthMargin<self.pos1[0])and(self.pos1[0]<self.viewWidth-self.widthMargin))and((self.heightMargin<self.pos1[1])and(self.pos1[1]<self.viewHeight-self.heightMargin))):
            if (self.paintingEnabled==True):
                self.mousePressedForPainting=True
                self.paintEventEnabled=True
                self.update()

            elif (self.createTemplateEnabled==True):
                self.mousePressedForCreatingTemplate=True
                self.createTemplateEventEnabled=True
                self.update()
            else:
                if self.drawRect==False:
                    self.listOfItems=self.items()
                    for item in self.listOfItems:
                        if (isinstance(item, QGraphicsRectItem)):
                            item.setBrush(QBrush(QtCore.Qt.transparent, style = QtCore.Qt.BDiagPattern))
                            item.setOpacity(0.3)
                    if (isinstance(self.itemAt(event.pos()), QGraphicsRectItem)):
                        self.selectedItem=self.itemAt(event.pos())
                        self.selectedItem.setBrush(QBrush(QtCore.Qt.yellow, style = QtCore.Qt.BDiagPattern))
                        self.selectedItem.setOpacity(0.15)
                        self.itemSelected=True
                        self.selectedIndex=self.selectedItem.data(self.scene.NameItem)
                        self.itemSelectionChangedSignal.emit(self.selectedIndex)
                        self.itemToBeMoved=self.itemAt(event.pos())
                        self.itemAtZero_x=self.itemToBeMoved.rect().x()
                        self.itemAtZero_y=self.itemToBeMoved.rect().y()
                        self.itemAtZero_width=self.itemToBeMoved.rect().width()
                        self.itemAtZero_height=self.itemToBeMoved.rect().height()
                        self.temp_x=self.pos1[0]
                        self.temp_y=self.pos1[1]
                        self.rectItemPressed=True
                        self.changeOnX=0
                        self.changeOnY=0

                    if (isinstance(self.itemAt(event.pos()), QGraphicsPixmapItem)):
                        self.itemSelected=False
                        self.mousePressedOnNoItemSignal.emit()


                    if (self.rectResized==False):
                        if (isinstance(self.itemAt(event.pos()), QGraphicsEllipseItem)):
                            self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
                            self.ellipseItemMousePressed=self.itemAt(event.pos())
                            self.ellipseItemToBeMoved=self.itemAt(event.pos())
                            self.ellipseItemAtZero_x=self.ellipseItemMousePressed.rect().x()
                            self.ellipseItemAtZero_y=self.ellipseItemMousePressed.rect().y()
                            self.ellipseItemAtZero_width=self.ellipseItemMousePressed.rect().width()
                            self.ellipseItemAtZero_height=self.ellipseItemMousePressed.rect().height()
                            self.indexOfellipseItemMousePressed=self.ellipseItemMousePressed.data(self.scene.NameItem)
                            self.tempForEllipse_x=self.pos1[0]
                            self.tempForEllipse_y=self.pos1[1]

                            for item in self.listOfItems:
                                if (isinstance(item, QGraphicsRectItem)&(self.indexOfellipseItemMousePressed==item.data(self.scene.NameItem))):
                                    self.rectItemToBeResized=item
                                    self.selectedItem=self.rectItemToBeResized
                                    self.selectedIndex=self.selectedItem.data(self.scene.NameItem)
                                    self.itemSelectionChangedSignal.emit(self.selectedIndex)
                            self.resizedItemAtZero_x=self.rectItemToBeResized.rect().x()
                            self.resizedItemAtZero_y=self.rectItemToBeResized.rect().y()
                            self.resizedItemAtZero_width=self.rectItemToBeResized.rect().width()
                            self.resizedItemAtZero_height=self.rectItemToBeResized.rect().height()
                            self.ellipseItemPressed=True


                else:
                    self.oldPos = self.mapToScene(event.pos())
                    self.mousePressedForRect=True


    @Slot()
    def mouseMoveEvent(self,event):
        self.pos2[0], self.pos2[1] = event.pos().x(), event.pos().y()
        if(((self.widthMargin<self.pos2[0])and(self.pos2[0]<self.viewWidth-self.widthMargin))and((self.heightMargin<self.pos2[1])and(self.pos2[1]<self.viewHeight-self.heightMargin))):

            if (self.paintingEnabled==True):     #painting kısmı
                self.paintPos = self.mapToScene(event.pos())
                self.listOfItems=self.items()
                self.listOfItems[0].setBrush(QBrush(self.paintingColor, style = QtCore.Qt.BDiagPattern))
                self.listOfItems[0].setPen(QtGui.QPen(self.paintingColor))
                self.listOfItems[0].setRect(self.paintPos.x(), self.paintPos.y(), self.painterSize, self.painterSize)   
                self.update()
                self.setCursor(QCursor(QtCore.Qt.BlankCursor))

                if (self.mousePressedForPainting==True):
                    self.paintEventEnabled=True
                    self.update()

            elif (self.createTemplateEnabled==True):                #Template kısmı
                print ("create temp")
                self.paintPos = self.mapToScene(event.pos())
                self.listOfItems=self.items()
                self.paintPos = self.mapToScene(event.pos())
                self.listOfItems[0].setBrush(QBrush(self.paintingColor, style = QtCore.Qt.BDiagPattern))
                self.listOfItems[0].setPen(QtGui.QPen(self.paintingColor))
                self.listOfItems[0].setRect(self.paintPos.x(), self.paintPos.y(), self.painterSize, self.painterSize)
                self.update()
                self.setCursor(QCursor(QtCore.Qt.BlankCursor))
                if (self.mousePressedForCreatingTemplate==True):
                    self.createTemplateEventEnabled=True
                    self.update()

            else:                               # diğerleri
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                self.listOfItems=self.items()
                for item in self.listOfItems:
                    if (isinstance(item, QGraphicsRectItem)):
                        item.setBrush(QBrush(QtCore.Qt.transparent, style = QtCore.Qt.BDiagPattern))

                for item in self.listOfItems:
                    if (isinstance(item, QGraphicsEllipseItem)):
                        item.setBrush(QBrush(QtCore.Qt.yellow, style = QtCore.Qt.BDiagPattern))


                if (isinstance(self.itemAt(event.pos()), QGraphicsRectItem)):
                    self.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
                    item=self.itemAt(event.pos())
                    item.setBrush(QBrush(QtCore.Qt.blue, style = QtCore.Qt.BDiagPattern))
                    item.setOpacity(0.3)

                if (self.itemSelected==True):
                    for item in self.listOfItems:
                        if (isinstance(item, QGraphicsRectItem)&(self.selectedIndex==item.data(self.scene.NameItem))):
                            item.setBrush(QBrush(QtCore.Qt.yellow, style = QtCore.Qt.BDiagPattern))
                            item.setOpacity(0.15)

                if (isinstance(self.itemAt(event.pos()), QGraphicsEllipseItem)):
                    self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
                    self.ellipseItemUnderMouse=self.itemAt(event.pos())
                    self.indexOfellipseItemUnderMouse=self.ellipseItemUnderMouse.data(self.scene.NameItem)
                    for item in self.listOfItems:
                        if (isinstance(item, QGraphicsEllipseItem)&(self.indexOfellipseItemUnderMouse==item.data(self.scene.NameItem))):
                            item.setBrush(QBrush(QtCore.Qt.red, style = QtCore.Qt.BDiagPattern))

                if self.drawRect==True:       # drawing rectangle
                    self.listOfItems=self.items()

                    self.setCursor(QCursor(QtCore.Qt.CrossCursor))
                    self.newPos = self.mapToScene(event.pos())
                    self.listOfItems[1].setLine(self.newPos.x(), 0, self.newPos.x(), self.viewHeight)
                    self.listOfItems[2].setLine(0, self.newPos.y(), self.viewWidth, self.newPos.y())

                    if self.mousePressedForRect==True: # creating rectangle
                        self.newPos = self.mapToScene(event.pos())
                        if (self.newPos.x()>self.oldPos.x())&(self.newPos.y()>self.oldPos.y()):
                            self.listOfItems[0].setRect(self.oldPos.x(),self.oldPos.y(), abs(self.oldPos.x()-self.newPos.x()), abs(self.oldPos.y()-self.newPos.y()))
                        elif (self.newPos.x()>self.oldPos.x())&(self.newPos.y()<self.oldPos.y()):
                            self.listOfItems[0].setRect(self.oldPos.x(),self.newPos.y(), abs(self.oldPos.x()-self.newPos.x()), abs(self.oldPos.y()-self.newPos.y()))
                        elif (self.newPos.x()<self.oldPos.x())&(self.newPos.y()>self.oldPos.y()):
                            self.listOfItems[0].setRect(self.newPos.x(),self.oldPos.y(), abs(self.oldPos.x()-self.newPos.x()), abs(self.oldPos.y()-self.newPos.y()))
                        else:
                            self.listOfItems[0].setRect(self.newPos.x(),self.newPos.y(), abs(self.newPos.x()-self.oldPos.x()), abs(self.newPos.y()-self.oldPos.y()))

                        self.mouseMovedForDrawing=True
                        self.update()

                if self.rectItemPressed==True:     # moving the rectangle
                    self.changeOnX=(float(self.pos2[0]-self.temp_x)/self.graphScale)
                    self.changeOnY=(float(self.pos2[1]-self.temp_y)/self.graphScale)
                    if(((self.itemAtZero_x+self.changeOnX)>0)&((self.itemAtZero_y+self.changeOnY)>0)&((self.itemAtZero_x+self.changeOnX+self.itemAtZero_width)<(self.sceneWidth))&((self.itemAtZero_y+self.changeOnY+self.itemAtZero_height)<(self.sceneHeight))):
                        self.itemToBeMoved.setRect((self.itemAtZero_x+self.changeOnX), (self.itemAtZero_y+self.changeOnY), self.itemAtZero_width, self.itemAtZero_height)
                    listOfLinkedEllipseItems=[]
                    for item in self.listOfItems:
                        if (isinstance(item, QGraphicsEllipseItem)&(self.selectedIndex==item.data(self.scene.NameItem))):
                            listOfLinkedEllipseItems.append(item)

                    listOfLinkedEllipseItems[0].setRect(self.itemToBeMoved.rect().x()-self.ellipseRadius/2,self.itemToBeMoved.rect().y()-self.ellipseRadius/2,self.ellipseRadius,self.ellipseRadius)
                    listOfLinkedEllipseItems[1].setRect(self.itemToBeMoved.rect().x()+self.itemToBeMoved.rect().width()-self.ellipseRadius/2,self.itemToBeMoved.rect().y()-self.ellipseRadius/2,self.ellipseRadius,self.ellipseRadius)
                    listOfLinkedEllipseItems[2].setRect(self.itemToBeMoved.rect().x()-self.ellipseRadius/2,self.itemToBeMoved.rect().y()+self.itemToBeMoved.rect().height()-self.ellipseRadius/2,self.ellipseRadius,self.ellipseRadius)
                    listOfLinkedEllipseItems[3].setRect(self.itemToBeMoved.rect().x()+self.itemToBeMoved.rect().width()-self.ellipseRadius/2,self.itemToBeMoved.rect().y()+self.itemToBeMoved.rect().height()-self.ellipseRadius/2,self.ellipseRadius,self.ellipseRadius)
                    self.rectMoved=True
                    self.update()

                if ((self.ellipseItemPressed==True)&(isinstance(self.itemAt(event.pos()), QGraphicsEllipseItem))):  #resizing the rectangle

                    self.indexOfellipseItemToBeMoved=self.ellipseItemToBeMoved.data(self.scene.NameItem)
                    for item in self.listOfItems:
                        if (isinstance(item, QGraphicsEllipseItem)&(self.indexOfellipseItemToBeMoved==item.data(self.scene.NameItem))):
                            #right top
                            if ((item.rect().x()>self.rectItemToBeResized.rect().x())&(item.rect().y()<self.rectItemToBeResized.rect().y())):
                                self.rightTopEllipseItem=item
                            #right bottom
                            if ((item.rect().x()>self.rectItemToBeResized.rect().x())&(item.rect().y()>self.rectItemToBeResized.rect().y())):
                                self.rightBottomEllipseItem=item
                            #left top
                            if ((item.rect().x()<self.rectItemToBeResized.rect().x())&(item.rect().y()<self.rectItemToBeResized.rect().y())):
                                self.leftTopEllipseItem=item
                            #left bottom
                            if ((item.rect().x()<self.rectItemToBeResized.rect().x())&(item.rect().y()>self.rectItemToBeResized.rect().y())):
                                self.leftBottomEllipseItem=item

                    self.changeOnX=(float(self.pos2[0]-self.tempForEllipse_x)/self.graphScale)  #convertion from view to scene
                    self.changeOnY=(float(self.pos2[1]-self.tempForEllipse_y)/self.graphScale)
                    self.ellipseItemToBeMoved.setRect(self.ellipseItemAtZero_x+self.changeOnX, self.ellipseItemAtZero_y+self.changeOnY, self.ellipseItemAtZero_width, self.ellipseItemAtZero_height )
                    theItem=self.rectItemToBeResized
                    leftBot=self.leftBottomEllipseItem
                    leftTop=self.leftTopEllipseItem
                    rightBot=self.rightBottomEllipseItem
                    rightTop=self.rightTopEllipseItem
                    mPress=self.ellipseItemMousePressed
                    radi=self.ellipseRadius
                    zero_x=self.resizedItemAtZero_x
                    zero_y=self.resizedItemAtZero_y
                    zero_width=self.resizedItemAtZero_width
                    zero_height=self.resizedItemAtZero_height
                    #right top

                    if ((mPress.rect().x()>theItem.rect().x())&(mPress.rect().y()<theItem.rect().y())):
                        if ((self.changeOnX-radi>(-zero_width))&(self.changeOnY+radi<zero_height)):
                            theItem.setRect(zero_x, zero_y+self.changeOnY, zero_width+self.changeOnX, zero_height-self.changeOnY)
                            leftTop.setRect(theItem.rect().x()-radi/2, theItem.rect().y()-radi/2, radi, radi)
                            rightBot.setRect(theItem.rect().x()+theItem.rect().width()-radi/2, theItem.rect().y()+theItem.rect().height()-radi/2, radi, radi)
                        else:
                            self.ellipseItemPressed=False

                    #right bottom
                    if ((mPress.rect().x()>theItem.rect().x())&(mPress.rect().y()>theItem.rect().y())):
                        if ((self.changeOnX-radi>(-zero_width))&(self.changeOnY-radi>(-zero_height))):
                            theItem.setRect(zero_x, zero_y, zero_width+self.changeOnX, zero_height+self.changeOnY)
                            rightTop.setRect(theItem.rect().x()+theItem.rect().width()-radi/2, theItem.rect().y()-radi/2, radi, radi)
                            leftBot.setRect(theItem.rect().x()-radi/2, theItem.rect().y()+theItem.rect().height()-radi/2, radi, radi)
                        else:
                            self.ellipseItemPressed=False

                    #left top
                    if ((mPress.rect().x()<theItem.rect().x())&(mPress.rect().y()<theItem.rect().y())):
                        if ((self.changeOnX+radi<(zero_width))&(self.changeOnY+radi<(zero_height))):
                            theItem.setRect(zero_x+self.changeOnX, zero_y+self.changeOnY, zero_width-self.changeOnX, zero_height-self.changeOnY)
                            leftBot.setRect(theItem.rect().x()-radi/2, theItem.rect().y()+theItem.rect().height()-radi/2, radi, radi)
                            rightTop.setRect(theItem.rect().x()+theItem.rect().width()-radi/2, theItem.rect().y()-radi/2, radi, radi)
                        else:
                            self.ellipseItemPressed=False

                    #left bottom
                    if ((mPress.rect().x()<theItem.rect().x())&(mPress.rect().y()>theItem.rect().y())):
                        if ((self.changeOnX+radi<(zero_width))&(self.changeOnY-radi>(-zero_height))):
                            theItem.setRect(zero_x+self.changeOnX, zero_y, zero_width-self.changeOnX, zero_height+self.changeOnY)
                            leftTop.setRect(theItem.rect().x()-radi/2, theItem.rect().y()-radi/2, radi, radi)
                            rightBot.setRect(theItem.rect().x()+theItem.rect().width()-radi/2, theItem.rect().y()+theItem.rect().height()-radi/2,radi,self.ellipseRadius)
                        else:
                            self.ellipseItemPressed=False

                    self.update()
                    self.rectResized=True
                    self.ellipseItemPressed==False
    @Slot()
    def mouseReleaseEvent(self, event):
        print ("release")
        self.paintEventEnabled=False
        self.createTemplateEventEnabled=False
        self.mousePressedForPainting=False
        self.mousePressedForCreatingTemplate=False

        if ((self.paintingEnabled==False)and(self.createTemplateEnabled==False)):
            self.ellipseItemPressed==False
            self.mousePressedForRect=False
            self.rectItemPressed=False

            if (self.drawRect==True)&(self.mouseMovedForDrawing==False): # drawing rectangle
                self.update()
                self.drawRect=False
                self.mouseMovedForDrawing=False
                self.setUpWindowSignal.emit()
                self.scale(self.netZoomFactor, self.netZoomFactor)
                self.viewSettingsChanged()

            if (self.drawRect==True)&(self.mouseMovedForDrawing==True): # drawing rectangle
                newPos_x=self.newPos.x()
                newPos_y=self.newPos.y()
                if (event.pos().x()>self.viewWidth):
                    newPos_x=self.sceneWidth
                if (event.pos().y()>self.viewHeight):
                    newPos_y=self.sceneHeight
                if (event.pos().x()<0):
                    newPos_x=0
                if (event.pos().y()<0):
                    newPos_y=0
                if (self.newPos.x()>self.oldPos.x())&(self.newPos.y()>self.oldPos.y()):
                    self.createdRectPositionSignal.emit(self.oldPos.x(),self.oldPos.y(), abs(self.oldPos.x()-self.newPos.x()), abs(self.oldPos.y()-self.newPos.y()))
                elif (self.newPos.x()>self.oldPos.x())&(self.newPos.y()<self.oldPos.y()):
                    self.createdRectPositionSignal.emit(self.oldPos.x(),self.newPos.y(), abs(self.oldPos.x()-self.newPos.x()), abs(self.oldPos.y()-self.newPos.y()))
                elif (self.newPos.x()<self.oldPos.x())&(self.newPos.y()>self.oldPos.y()):
                    self.createdRectPositionSignal.emit(self.newPos.x(),self.oldPos.y(), abs(self.oldPos.x()-self.newPos.x()), abs(self.oldPos.y()-self.newPos.y()))
                else:
                    self.createdRectPositionSignal.emit(self.newPos.x(),self.newPos.y(), abs(self.newPos.x()-self.oldPos.x()), abs(self.newPos.y()-self.oldPos.y()))

                self.enableIdInputOfCreatedRectSignal.emit()
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
                self.update()
                self.drawRect=False
                self.mouseMovedForDrawing=False
                if (self.advancedMode==True):
                    self.jumpToCreateRectAppSinal.emit(True)

            if (self.rectMoved==True): #moving rectangle
                self.movedRectPositionSignal.emit((self.itemToBeMoved.rect().x()), (self.itemToBeMoved.rect().y()), self.itemToBeMoved.rect().width(), self.itemToBeMoved.rect().height())
                self.rectMoved=False

            if (self.rectResized==True): #resizing the rectangle
                self.ellipseItemPressed=False
                self.resizedRectPositionalSignal.emit(self.rectItemToBeResized.rect().x(), self.rectItemToBeResized.rect().y(), self.rectItemToBeResized.rect().width(), self.rectItemToBeResized.rect().height())
                print ("rectResized")
                self.rectResized=False

class PSLGraphicsView(QGraphicsView):
    polygonPointsSignal=Signal(int,int)
    def __init__(self,pslScene):
        QGraphicsView.__init__(self)
        self.setScene(pslScene)
        self.scene=pslScene
        self.drawingPolygonEnabled = False
        self.polygonIndex = 0
        self.polygon=[]
        self.polygonArray=[]
        self.polygonArray.append(self.polygon)

    def mousePressEvent(self, event):
        self.scenePos = self.mapToScene(event.pos())
        if self.drawingPolygonEnabled==True:
            self.point = (int(self.scenePos.x()), int(self.scenePos.y()))
            self.polygonPointsSignal.emit(self.point[0], self.point[1])
            self.polygon=self.polygonArray[self.polygonIndex]
            self.polygon.append(self.point)
            self.polygonArray[self.polygonIndex]=self.polygon
            print (self.polygonArray)
            self.drawPolygons()

    def deletePolygons(self):
        self.drawingPolygonEnabled = False
        self.polygonIndex = 0
        self.polygon = []
        self.polygonArray = list()
        self.polygonArray.append(self.polygon)
        self.listOfItems = self.items()
        for item in self.listOfItems:
            if (isinstance(item, QGraphicsLineItem)):
                self.scene.removeItem(item)

    def drawPolygons(self):
        # draw polygons
        if self.polygonArray:
            for i in range(len(self.polygonArray)):
                if len(self.polygonArray[i]) > 1:
                    self.polygon = self.polygonArray[i]
                    for j in range(len(self.polygon) - 1):
                        self.lineItem = QGraphicsLineItem()
                        self.lineItem.setLine(self.polygon[j][0], self.polygon[j][1], self.polygon[j + 1][0],self.polygon[j + 1][1])
                        self.scene.addItem(self.lineItem)