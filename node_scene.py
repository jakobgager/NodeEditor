from node_graphics_scene import QNEGraphicsScene
from node_node import Node
from node_edge import Edge

class Scene():
    def __init__(self):
        self.nodes = []
        self.edges = []
        
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
        self.edges.remove(edge)