from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_graphics_scene import QNEGraphicsScene
from node_graphics_socket import QNEGraphicsSocket
from node_graphics_edge import QNEGraphicsEdge
from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_cutline import QNECutLine

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_TRESHOLD = 10
DEBUG = True

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
        self.editingFlag = False

        # cutline
        self.cutline = QNECutLine()
        self.grScene.addItem(self.cutline)

    ##########
    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        #self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

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
        if DEBUG: print('LMB Click', item, self.debug_modifiers(event))
        if hasattr(item, 'node') or isinstance(item, QNEGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.buttons() | Qt.LeftButton, 
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return
        if type(item) is QNEGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        if item is None:
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
        super().mousePressEvent(event)

    ##########
    def leftMouseButtonRelease(self, event:QMouseEvent):
        item = self.getItemAtClick(event)
        self.new_lmb_click_scene_pos = self.mapToScene(event.pos())
        dist_scene = self.new_lmb_click_scene_pos - self.last_lmb_click_scene_pos
        if hasattr(item, 'node') or isinstance(item, QNEGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, 
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return
        if self.mode == MODE_EDGE_DRAG:
            if (dist_scene.x()**2 + dist_scene.y()**2) > EDGE_DRAG_START_TRESHOLD**2:
                res = self.edgeDragEnd(item)
                if res: return
        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.grScene.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return
        super().mouseReleaseEvent(event)

    ##########
    def rightMouseButtonPress(self, event:QMouseEvent):
        super().mousePressEvent(event)
        item = self.getItemAtClick(event)
        if DEBUG:
            if isinstance(item, QNEGraphicsEdge):
                print(item.edge)
            if type(item) is QNEGraphicsSocket:
                print(item.socket, 'has edge', item.socket.edge)

            if item is None:
                print('Scene:')
                print('Mode:', self.mode)
                print('  Nodes:')
                for node in self.grScene.scene.nodes: print('    ', node)
                print('  Edges:')
                for edge in self.grScene.scene.edges: print('    ', edge)


    ##########
    def rightMouseButtonRelease(self, event:QMouseEvent):
        super().mouseReleaseEvent(event)


    ##########
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()
        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.grScene.update()

        super().mouseMoveEvent(event)

    ##########
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete:
            if not self.editingFlag:
                self.deleteSelected()
                return
        elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
            self.grScene.scene.saveToFile('graph.json')
        elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier:
            self.grScene.scene.loadFromFile('graph.json')
        elif event.key() == Qt.Key_1:
            self.grScene.scene.history.storeHistory('Item A')
        elif event.key() == Qt.Key_2:
            self.grScene.scene.history.storeHistory('Item B')
        elif event.key() == Qt.Key_3:
            self.grScene.scene.history.storeHistory('Item C')
        elif event.key() == Qt.Key_4:
            self.grScene.scene.history.undo()
        elif event.key() == Qt.Key_5:
            self.grScene.scene.history.redo()
        elif event.key() == Qt.Key_H:
            print('History:   len({0})'.format(len(self.grScene.scene.history.history_stack)),
                '-- current step:', self.grScene.scene.history.history_current_step)
            print(self.grScene.scene.history.history_stack)
        else:
            super().keyPressEvent(event)

    ##########
    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QNEGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

    ##########
    def cutIntersectingEdges(self):
        for ix in range(len(self.cutline.line_points)-1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix+1]

            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()

    ##########
    def debug_modifiers(self, event:QEvent):
        out = 'MODS: '
        if event.modifiers() & Qt.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.AltModifier: out += "ALT "
        if event.modifiers() & Qt.ControlModifier: out += "CTRL "
        return out

    ##########
    def getItemAtClick(self, event:QMouseEvent):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    ##########
    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart ~ Start dragging edge')
        if DEBUG: print('View::edgeDragStart ~   assign Start Socket to', item.socket)
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, edge_type=EDGE_TYPE_BEZIER)
        if DEBUG: print('View::edgeDragStart ~   dragEdge:', self.dragEdge)

    ##########
    def edgeDragEnd(self, item):
        """return True if skip the rest of the code"""
        self.mode = MODE_NOOP
        if type(item) is QNEGraphicsSocket:
            if item.socket != self.last_start_socket:
                if DEBUG: print('View::edgeDragEnd ~   assign End Socket', item.socket)
                if item.socket.hasEdge():
                    item.socket.edge.remove()
                if self.previousEdge is not None:
                    self.previousEdge.remove()
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.updatePositions()
                return True

        if DEBUG: print('View::edgeDragEnd ~ End dragging edge')
        self.dragEdge.remove()
        self.dragEdge = None
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        if DEBUG: print('View::edgeDragEnd ~ everything done')
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

