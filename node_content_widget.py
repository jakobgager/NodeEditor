from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import node_node

class QNENodeContentWidget(QWidget):
    def __init__(self, node: 'node_node.Node', parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    ##########
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel('Some Title')
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QNETextEdit('foo'))

    ##########
    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editingFlag = value


class QNETextEdit(QTextEdit):
    
    ##########
    def focusInEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(True)
        return super().focusInEvent(event)
    
    ##########
    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().setEditingFlag(False)
        return super().focusOutEvent(event)