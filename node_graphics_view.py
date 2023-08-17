from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class QNEGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 0
        self.zoomStep = 1
        self.zoomRange = [-6, 6]

    ##########
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        #self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    ##########
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    
    ##########
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    ##########
    def middleMouseButtonPress(self, event: QMouseEvent):
        #print('MMB pressed')
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.MiddleButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                   Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)


    ##########
    def middleMouseButtonRelease(self, event: QMouseEvent):
        #print('MMB released')
        fakeRelease = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeRelease)
        self.setDragMode(QGraphicsView.NoDrag)

    ##########
    def leftMouseButtonPress(self, event:QMouseEvent):
        return super().mousePressEvent(event)

    ##########
    def leftMouseButtonRelease(self, event:QMouseEvent):
        return super().mouseReleaseEvent(event)

    ##########
    def rightMouseButtonPress(self, event:QMouseEvent):
        return super().mousePressEvent(event)

    ##########
    def rightMouseButtonRelease(self, event:QMouseEvent):
        return super().mouseReleaseEvent(event)

    ### Handle mouse wheel event
    ##########
    def wheelEvent(self, event: QWheelEvent) -> None:
        # calculate zoom out factor
        zoomOutFactor = 1/self.zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
            angledir = 1
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
            angledir = -1

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom = self.zoomRange[0]
            clamped = True
        if self.zoom > self.zoomRange[1]:
            self.zoom = self.zoomRange[1]
            clamped = True
        
        # set scene scale
        if not clamped or self.zoomClamp == False:
            self.scale(zoomFactor, zoomFactor)        
            angle = angledir*10
            self.rotate(angle)

