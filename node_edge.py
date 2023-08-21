import node_socket
import node_scene
from node_graphics_edge import *

__all__ = ['EDGE_TYPE_DIRECT', 'EDGE_TYPE_BEZIER', 'Edge']

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge():
    def __init__(self, scene: 'node_scene.Scene', start_socket:'node_socket.Socket', end_socket:'node_socket.Socket', edge_type=EDGE_TYPE_DIRECT):
        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.start_socket.setConnectedEdge(self)
        if end_socket is not None:
            self.end_socket.setConnectedEdge(self)
        self.scene.addEdge(self)
        self.grEdge = QNEGraphicsEdgeDirect(self) if edge_type==EDGE_TYPE_DIRECT else QNEGraphicsEdgeBezier(self)
        self.updatePositions()
        #print('Edge: ', self.grEdge.posSource, ' to ', self.grEdge.posDestination)
        # inject edge to scene
        self.scene.grScene.addItem(self.grEdge)

    ##########
    def __str__(self):
        return 'Edge <{0}> connecting {1} <-> {2}'.format(hex(id(self)), self.start_socket, self.end_socket)

    ##########
    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)

        #print(' SS:', self.start_socket)
        #print(' ES:', self.end_socket)
        self.grEdge.update()

    ##########
    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.start_socket = None
        self.end_socket = None
    
    ##########
    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)