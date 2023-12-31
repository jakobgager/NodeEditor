from collections import OrderedDict

from node_serializable import Serializable
import node_node
import node_edge
from node_graphics_socket import QNEGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket(Serializable):
    def __init__(self, node:'node_node.Node', index=0, position=LEFT_TOP, socket_type=1):
        super().__init__()
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type
        self.grSocket = QNEGraphicsSocket(self, self.socket_type)
        self.grSocket.setPos(*self.node.getSocketPosition(index, position))
        
        self.edge = None

    ##########
    def __str__(self):
        return 'Socket <{0}>'.format(hex(id(self)))

    ##########
    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    ##########
    def setConnectedEdge(self, edge:'node_edge.Edge'=None):
        self.edge = edge
    
    ##########
    def hasEdge(self):
        return self.edge is not None

    ##########
    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self.index), 
            ('position', self.position),
            ('socket_type', self.socket_type)
        ])
    
    ##########
    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self
        return True