import node_node
import node_edge
from node_graphics_socket import QNEGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket():
    def __init__(self, node:'node_node.Node', index=0, position=LEFT_TOP, socket_type=1):
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
