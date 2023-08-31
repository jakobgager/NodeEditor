from collections import OrderedDict
from typing import List

from node_serializable import Serializable
from node_graphics_node import QNEGraphicsNode
from node_content_widget import QNENodeContentWidget
from node_socket import *
import node_scene

class Node(Serializable):
    def __init__(self, scene:'node_scene.Scene', title='Undefined Node', inputs=[], outputs=[]):
        super().__init__()
        self.scene = scene
        self._title = title   # dummytitle required for graphics node initialization
        
        self.content = QNENodeContentWidget(self)
        self.grNode = QNEGraphicsNode(self)
        self.title = title
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
    def __str__(self):
        return 'Node <{0}> - {1}'.format(hex(id(self)), self.title)

    ##########
    @property
    def pos(self):
        return self.grNode.pos()   #QPoint .. pos.x
    
    ##########
    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    ##########
    @property
    def title(self): return self._title

    ##########
    @title.setter
    def title(self, value:str):
        self._title = value
        self.grNode.title = self._title

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
    
    ##########
    def remove(self):
        print('Removing Node', self)
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.remove()
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        self.scene.removeNode(self)

    ##########
    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs:
            inputs.append(socket.serialize())
        for socket in self.outputs:
            outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.grNode.scenePos().x()), 
            ('pos_y', self.grNode.scenePos().y()), 
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize())
        ])
    
    ##########
    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self

        self.title = data['title']
        self.setPos(data['pos_x'], data['pos_y'])
        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position']*10000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position']*10000)

        self.inputs = [] # type: List[Socket]
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], 
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap)
            self.inputs.append(new_socket)

        self.outputs = [] # type: List[Socket]
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'], 
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap)
            self.outputs.append(new_socket)
        return True