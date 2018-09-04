"""
Declares a point in a metric space.
"""
class Point:
    """
    Defines a point in a metric space.
    
    Parameters:
    ----------
    coords : Iterable
        The point coordinates.
    metric : Metric
        The metric used to measure points proximity.
    """
    def __init__(self, coords, metric):
        self.coords = coords
        self.metric = metric

    def distto(self, *others):
        """
        Computes the distance between points.
        
        Parameters:
        ----------
        others : variable length argument list of type Point.
        
        Returns:
        -------
        float or Decimal
            The minimum distance.
        """
        return self.metric.dist(self, *others)

    def __getitem__(self, index):
        """
        Returns the coordinate at position `index'.
        
        Parameters:
        ----------
        index : int
            The index of coordinate to be returned (starts from 0).
            
        Returns:
        -------
        float or Decimal
            The coordinate.
        """
        return self.coords[index]

    def __str__(self):
        """
        Creates a string representation for a point object.
        For example, for a point with coordinate 1,2,3 it returns '(1,2,3)'
        
        Parameters:
        ----------
        None
        
        Returns:
        -------
        str
        """
        return "(" + ", ".join(str(c) for c in self.coords) + ")"
    
    def __eq__(self, other):
        """
        Overloads the equality operator for point objects.
        Returns True if two points have the same coordinates.
        
        Parameters:
        ----------
        other : Point
            The right hand side point object.
        
        Returns:
        -------
        bool        
        """
        return self.coords == other.coords
    
    def __hash__(self):
        """
        Overloads the hash operation when used in a set or dictionary.
        The generated hash value is based on the coordinates of a point.
        
        Parameters:
        ----------
        None
        
        Returns:
        -------
        int
            The hash value.
        """
        return hash(tuple(self.coords))
    
    @staticmethod
    def importFrom(path, metric):
        points = []
        with open(path) as f:
            for line in f:
                points.append(Point([int(coord) if float(coord).is_integer() else float(coord) for coord in line.split(',')], metric))
        return points
    
    @staticmethod
    def exportTo(path, points):
        with open(path, 'w') as f:
            for point in points: f.write(', '.join([str(coord) for coord in point.coords]) + '\n')

def setMetric(metric, points):
    for pt in points: pt.metric = metric
