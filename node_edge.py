from collections import OrderedDict

from node_serializable import Serializable
import node_socket
import node_scene
from node_graphics_edge import *

__all__ = ['EDGE_TYPE_DIRECT', 'EDGE_TYPE_BEZIER', 'Edge']

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge(Serializable):
    def __init__(self, scene: 'node_scene.Scene', start_socket:'node_socket.Socket'=None, end_socket:'node_socket.Socket'=None, edge_type=EDGE_TYPE_DIRECT):
        super().__init__()
        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.addEdge(self)
        #print('Edge: ', self.grEdge.posSource, ' to ', self.grEdge.posDestination)

    ##########
    def __str__(self):
        return 'Edge <{0}> connecting {1} <-> {2}'.format(hex(id(self)), self.start_socket, self.end_socket)

    ##########
    @property
    def start_socket(self) -> node_socket.Socket: return self._start_socket

    ##########
    @start_socket.setter
    def start_socket(self, value: node_socket.Socket):
        self._start_socket = value
        if self.start_socket is not None:
            self.start_socket.edge = self

    ##########
    @property
    def end_socket(self) -> node_socket.Socket: return self._end_socket

    ##########
    @end_socket.setter
    def end_socket(self, value: node_socket.Socket):
        self._end_socket = value
        if self.end_socket is not None:
            self.end_socket.edge = self

    ##########
    @property
    def edge_type(self): return self._edge_type

    @edge_type.setter
    def edge_type(self, value):
        self._edge_type = value
        if hasattr(self, 'grEdge') and self.grEdge is not None:
            self.scene.grScene.removeItem(self.grEdge)
        if self.edge_type == EDGE_TYPE_DIRECT:
            self.grEdge = QNEGraphicsEdgeDirect(self)
        elif self.edge_type == EDGE_TYPE_BEZIER:
            self.grEdge = QNEGraphicsEdgeBezier(self)
        else:
            self.grEdge = QNEGraphicsEdgeBezier(self)
        # inject edge to scene
        self.scene.grScene.addItem(self.grEdge)
        if self.start_socket is not None:
            self.updatePositions()

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

    ##########
    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type), 
            ('start', self.start_socket.id),
            ('end', self.end_socket.id),
        ])
    
    ##########
    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type']
        return True