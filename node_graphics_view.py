from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_graphics_scene import QNEGraphicsScene
from node_graphics_socket import QNEGraphicsSocket

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_TRESHOLD = 10

class QNEGraphicsView(QGraphicsView):
    def __init__(self, grScene: QNEGraphicsScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 0
        self.zoomStep = 1
        self.zoomRange = [-6, 6]
        self.mode = MODE_NOOP

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
        item = self.getItemAtClick(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        self.lastitem = item
        if type(item) is QNEGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                print('Start dragging edge')
                print('  assign Start Socket')
                return
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        super().mousePressEvent(event)

    ##########
    def leftMouseButtonRelease(self, event:QMouseEvent):
        item = self.getItemAtClick(event)
        self.new_lmb_click_scene_pos = self.mapToScene(event.pos())
        dist_scene = self.new_lmb_click_scene_pos - self.last_lmb_click_scene_pos
        if item is not self.lastitem:
        #if (dist_scene.x()**2 + dist_scene.y()**2) > EDGE_DRAG_START_TRESHOLD**2:
            res = self.edgeDragEnd(item)
            if res: return
        super().mouseReleaseEvent(event)

    ##########
    def rightMouseButtonPress(self, event:QMouseEvent):
        super().mousePressEvent(event)

    ##########
    def rightMouseButtonRelease(self, event:QMouseEvent):
        super().mouseReleaseEvent(event)

    ##########
    def getItemAtClick(self, event:QMouseEvent):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    ##########
    def edgeDragEnd(self, item):
        """return True if skip the rest of the code"""
        self.mode = MODE_NOOP
        print('End dragging edge')
        if type(item) is QNEGraphicsSocket:
            print('  assign End Socket')
            return True
        return False


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

