"""
A base class for different point location algorithms
"""
from abc import ABC, abstractmethod
from node import dist, ch, rel
import functools

class PointLocation(ABC):
    def __init__(self, tree):
        self.tree = tree
        self.basictouchno=0
        self.splittouchno=0
        self.mergetouchno=0
        
    @abstractmethod
    def nn(self, point): 
        pass
    
    @abstractmethod
    def nndist(self, point, nn = None):
        pass
    
    @abstractmethod
    def removepoint(self, point):
        pass
    
    @abstractmethod
    def addnode(self, node):
        pass
    
    @abstractmethod
    def updateonremoval(self, node):
        pass
    
    @abstractmethod
    def updateoninsertion(self, node):
        pass
    
    @abstractmethod
    def updateonsplit(self, node):
        pass
    
class ParallelPointLocation(PointLocation):
    def __init__(self, tree, points):
        PointLocation.__init__(self, tree)
        
    def nn(self, point):
        child = self.tree.root.getchild()
        if dist(child,point) > self.tree.cr * self.tree.tau ** child.level:
            return self.tree.root
        return self.nnhelper(point, {child}, child.level) or self.tree.root
    
    def nnhelper(self, point, currentnodes, level):
        if len(currentnodes) != 0:
            self.basictouchno += len(currentnodes)
        if len(currentnodes) == 0 or \
            point.distto(*[n.point for n in currentnodes]) > self.tree.cr * self.tree.tau ** level:     
            return None
        children = ch(currentnodes)
        nextlevel = max(n.level for n in children)
        nextnodes = {n if n.level == nextlevel else n.par 
                     for n in children if dist(n, point) <= self.tree.cr * self.tree.tau ** nextlevel}
        self.basictouchno += len(children)
        nn = self.nnhelper(point, nextnodes, nextlevel)
        if nn:
            return nn
        self.basictouchno += len(currentnodes)
        return min(currentnodes, key = lambda n : point.distto(n.point))
    
#         return nn if nn else min(currentnodes, key = lambda n : point.distto(n.point))
    
    def nndist(self, point, nn = None):
        return dist(nn or self.nn(point), point)
    
    def removepoint(self, point): pass
    
    def addnode(self, node): pass
    
    def updateonremoval(self, node): pass
    
    def updateoninsertion(self, node): pass
    
    def updateonsplit(self, node): pass
    
class SinglePathPointLocation(PointLocation):
    def __init__(self, tree, points):
        PointLocation.__init__(self, tree)
        
    def nn(self, point):
        currentnode = self.tree.root
        nextnode = self.tree.root.getchild()
        self.basictouchno += 1
        while dist(nextnode, point) <= self.tree.cr * self.tree.tau ** nextnode.level:
            currentnode = nextnode
            allnodes = ch(rel(currentnode))
            nextlevel = max(n.level for n in allnodes)
            nextnode = min(allnodes, 
                           key = functools.partial(self.mincoveringdist, point = point, level = nextlevel))
        return currentnode
    
    def mincoveringdist(self, node, point, level):
        dst = dist(node, point)
        self.basictouchno += 1
        return dst if dst <= self.tree.cr * self.tree.tau ** level else float('inf')
    
    def nndist(self, point, nn = None):
        return dist(nn or self.nn(point), point)
    
    def removepoint(self, point): pass
    
    def addnode(self, node): pass
    
    def updateonremoval(self, node): pass
    
    def updateoninsertion(self, node): pass
    
    def updateonsplit(self, node): pass