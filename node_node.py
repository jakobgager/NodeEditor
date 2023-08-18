from node_graphics_node import QNEGraphicsNode
from node_content_widget import QNENodeContentWidget
from node_socket import *
from typing import List
import node_scene

class Node():
    def __init__(self, scene:'node_scene.Scene', title='Undefined Node', inputs=[], outputs=[]):
        self.scene = scene
        self.title = title
        
        self.content = QNENodeContentWidget()
        self.grNode = QNEGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22
        # create sockets for input and output
        self.inputs = [] # type: List[Socket]
        self.outputs = [] # type: List[Socket]
        for counter, item in enumerate(inputs, 0):
            self.inputs.append(Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item))
        for counter, item in enumerate(outputs, 0):
            self.outputs.append(Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item))
    
    ##########
    @property
    def pos(self):
        return self.grNode.pos()   #QPoint .. pos.x
    
    ##########
    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    ##########
    def getSocketPosition(self, index, position):
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = self.grNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing
        return [x,y]
    
    ##########
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()