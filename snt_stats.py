"""
Provides some statistics about a given net-tree.
"""

from config import config

class SNTStats:
    """
    Defines operations to report statistics for a given net-tree.
    
    Parameters:
    ----------
    T : SNT
        A semi-compressed net-tree.
    """
    def __init__(self, T):
        self.T = T
        self.levels = set()
        
    def nodeno(self):
        """
        Returns the number of nodes. It does not include the nodes at level 
        +infty, -infty and the highest level below +infty.
        
        Parameters:
        ----------
        None
        
        Returns:
        -------
        int
            The number of nodes in the net-tree.
        """
        return self.dfssearch(self.T.root.getchild(), lambda node:1) - 1
    
    def childno(self):
        """
        Returns the number of child links. It does not include -infty.
        
        Parameters:
        ----------
        None
        
        Returns:
        -------
        int
            The number of child links.
        """
        return self.dfssearch(self.T.root.getchild(),
                              lambda node:0 if node.getchild().level == config.arithmatic.ninfty else len(node.ch))
    
    def relno(self):
        """
        Returns the total number of relatives. It does not include the nodes at level 
        +infty, -infty and the highest level below +infty.
        
        Parameters:
        ----------
        None
        
        Returns:
        -------
        int
            The number of relative links.
        """
        return self.dfssearch(self.T.root.getchild(), lambda node:len(node.rel)) - 1
    
    # not count +infty, -infty and the highest level below +infty
    def levelno(self):
        """
        Returns the number of levels excluding +infty, -infty and the highest level below +infty.
        
        Parameters:
        ----------
        None
        
        Returns:
        -------
        int
            The number of relative links.
        """
        self.levels = set()
        return self.dfssearch(self.T.root.getchild(), self.levellambda) - 1
        
    def levellambda(self, node):
        if node.level in self.levels: return 0
        self.levels.add(node.level)
        return 1
    
    def jumpno(self):
        """
        Returns the number of long edges or jumps (compression) not counting edges from +infty and to -infty.
        
        Parameters:
        ----------
        None
        
        Returns:
        -------
        int
            The total number of levels.
        """
        return self.dfssearch(self.T.root.getchild(),
                              lambda node:1 if len(node.ch) == 1 and node.level > node.getchild().level + 1 and 
                              node.getchild().level != config.arithmatic.ninfty else 0)
        
    def dfssearch(self, node, lmda):        
        if node.level == config.arithmatic.ninfty:
            return 0
        if (node.ch) == 1 and node.getchild().level == config.arithmatic.ninfty: return lmda(node)      
        count = 0
        for ch in node.ch:
            count += self.dfssearch(ch, lmda)
        return count + lmda(node)
