"""
Defines nodes that are the building blocks of net-trees.
"""

from point import Point

class Node:
    """
    Defines a Node associated to a point and a level which also maintains 
    its parent, children, and relatives.
        
    Parameters
    ----------
    point : Point
        Associated point.
    level : int
        Associated level.
    """
    def __init__(self, point, level):
        self.point = point
        self.level = level
        self.par = None
        self.rel = {self}
        self.ch = set()

    def addrel(self, other):
        """
        Makes `self` and `other` relatives.
        
        Parameters
        ----------
        other: Node
            The relative node.
        
        Returns:
        -------
        None
        """
        self.rel.add(other)
        other.rel.add(self)

    def addch(self, other):
        """
        Adds `other` as a child of `self`, also sets `self` as the parent of `other`. 
               
        Parameters
        ----------
        other: Node
            The child node.
        
        Returns:
        -------
        None
        """
        if other.par: other.par.ch.discard(other)
        self.ch.add(other)
        other.par = self

    def setpar(self, other):
        """
        Makes `other` as the parent of `self`, also sets `self` as a child of `other`.  
              
        Parameters
        ----------
        other: Node
            The parent node.
        
        Returns:
        -------
        None
        """
        other.addch(self)

    def getchild(self):
        """
        Returns an arbitrary child.
                
        Parameters
        ----------
        None
        
        Returns:
        -------
        Node
            An arbitrary child of the current node.
        """
        return next(iter(self.ch))

    def __str__(self):
        return str(self.point) + " at level " + str(self.level) + "\n" + "".join(str(c) for c in self.ch)
    
    def __eq__(self, other):
        return self.point == other.point and self.level == other.level
    
    def __hash__(self):
        return hash((tuple(self.point.coords), self.level))

"""
Below are some static methods that allow us to treat the nodes as a metric
space, and also to access the par, ch, and rel of entire sets of nodes instead
of just individuals.
"""

def ch(nodes):
    return nodes.ch if isinstance(nodes, Node) else \
            set.union(*(node.ch for node in nodes))

def rel(nodes):
    return nodes.rel if isinstance(nodes, Node) else \
            set.union(*(node.rel for node in nodes))

def par(nodes):
    return nodes.par if isinstance(nodes, Node) else \
            {node.par for node in nodes if node.par is not None}

def nearest(node, others):        
    return min(others, key=lambda n:node.point.distto(n.point))

def dist(node, other):
    return node.point.distto(other if isinstance(other, Point) else other.point)
