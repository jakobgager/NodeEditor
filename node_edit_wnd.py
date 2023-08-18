from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_scene import Scene
from node_node import Node
from node_graphics_view import QNEGraphicsView
from node_edge import *

class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self._stylesheet_filename)

        self.initUI()

    ##########
    def initUI(self):
        self.setGeometry(200, 200, 800, 640)
        self.setWindowTitle('Node Editor')

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        # create Scene
        self.scene = Scene()

        self.addNodes()

        # GraphicsView
        self.view = QNEGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)
        
        self.show()

        #self.addDebugContent()

    ##########
    def loadStylesheet(self, filename):
        print('Style loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    ##########
    def addNodes(self):
        node1 = Node(self.scene, 'My Awesome Node 1', inputs=[0,2], outputs=[4])
        node2 = Node(self.scene, 'My Awesome Node 2', inputs=[0,4,5], outputs=[4])
        node3 = Node(self.scene, 'My Awesome Node 3', inputs=[1,2,3,0], outputs=[4])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)
        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)

    ##########
    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText('Some Text adsf', QFont('Ubuntu'))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 0.7, 1.0))

        widget1 = QPushButton('Button1')
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 100)

        line = self.grScene.addLine(-200, -100, 400, 200, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
        line.setFlag(QGraphicsItem.ItemIsMovable)