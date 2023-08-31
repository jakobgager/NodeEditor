from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import List

class QNECutLine(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_points = [] # type: List[QPointF]
        self._pen = QPen(Qt.white)
        self._pen.setWidthF(2.0)
        self._pen.setDashPattern([3,3])
        # always on top
        self.setZValue(2)

    def boundingRect(self) -> QRectF:
        return QRectF(0,0,1,1)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget=None) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)
        poly = QPolygonF(self.line_points)
        painter.drawPolyline(poly)