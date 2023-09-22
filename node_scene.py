import json
from collections import OrderedDict
from typing import List

from node_serializable import Serializable
from node_graphics_scene import QNEGraphicsScene
from node_node import Node
from node_edge import Edge
from node_scene_history import SceneHistory

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = [] # type: List[Node]
        self.edges = [] # type: List[Edge]
        
        self.scene_width = 6400
        self.scene_height = 6400

        self.initUI()
        self.history = SceneHistory(self)

    ##########
    def initUI(self):
        self.grScene = QNEGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    ##########
    def addNode(self, node: Node):
        self.nodes.append(node)

    ##########
    def addEdge(self, edge: Edge):
        self.edges.append(edge)
    
    
    ##########
    def removeNode(self, node: Node):
        self.nodes.remove(node)

    ##########
    def removeEdge(self, edge: Edge):
        if edge in self.edges:
            self.edges.remove(edge)

    ##########
    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

    ##########
    def saveToFile(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))
        print('saving to', filename, 'was successful')
            
    ##########
    def loadFromFile(self, filename):
        with open(filename, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)

    ##########
    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes:
            nodes.append(node.serialize())
        for edge in self.edges:
            edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes), 
            ('edges', edges)
        ])
    
    ##########
    def deserialize(self, data, hashmap={}):
        print('Deserialization data', data)

        self.clear()
        hashmap = {}
        # create node
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap=hashmap)

        # create edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap=hashmap) 
        return True