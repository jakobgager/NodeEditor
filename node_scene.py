import json
from collections import OrderedDict
from typing import List

from node_serializable import Serializable
from node_graphics_scene import QNEGraphicsScene
from node_node import Node
from node_edge import Edge

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = [] # type: List[Node]
        self.edges = [] # type: List[Edge]
        
        self.scene_width = 6400
        self.scene_height = 6400

        self.initUI()

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
    def saveToFile(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))
        print('saving to', filename, 'was successful')
            
    ##########
    def loadFromFile(self, filename):
        with open(filename, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
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
        return False