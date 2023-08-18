from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import node_edge

class QNEGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge:'node_edge.Edge', parent=None):
        super().__init__(parent)
        self.edge = edge
        self.color = QColor('#001000')
        self._pen = QPen(self.color)
        self._pen.setWidth(2.0)
        self.color_selected = QColor('#00ff00')
        self._pen_selected = QPen(self.color_selected)
        self._pen_selected.setWidth(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]

    ##########
    def setSource(self, x, y):
        self.posSource = [x,y]

    ##########
    def setDestination(self, x, y):
        self.posDestination = [x,y]

    ##########
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget=None) -> None:
        self.updatePath()
        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    ##########
    def updatePath(self):
        """Will handle drawing QPainterPath from Point A to B"""
        raise NotImplemented('This method has to be overwritten')


###############
class QNEGraphicsEdgeDirect(QNEGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0],self.posDestination[1])
        self.setPath(path)


###############
class QNEGraphicsEdgeBezier(QNEGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]:
            dist *= -1
        
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + dist, s[1],
                     d[0] - dist, d[1],
                     self.posDestination[0],self.posDestination[1])
        self.setPath(path)
