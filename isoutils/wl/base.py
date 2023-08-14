import numpy as np
from ..utils import MultiSet, AdjList
from typing import Literal
from scipy.stats import rankdata

class BaseWL:
    """
    Base solver class for all WL-type algorithms.

    A WL-type algorithm is defined as following:
        * The algorithm maintains a "color list", each of whose entries is a 
        color assigned to one particular structure of the graph. 
        * Each entry of the "color list" is updated by aggregating the colors
        from other parts of the list.
        * After a stable coloring is reached, i.e. the "color list" no longer
        changes after a further update, the stable coloring is converted to a
        multiset as the final representation of the graph.

    Therefore, to specify a WL-type algorithm, only three things are to clarify:
        * How to initialize the "color list". This includes two questions, 
        namely (i) what is the meaning of the color, and (ii) what is the rule
        to generate initial coloring.
        * How to update the "color list". This requires specifying where to
        aggregate color from, and how to use the aggregated colors.
        * How to pool the "color list" into a representation of the graph.

    To define a WL-type algorithm, three methods have to be implemented, namely
    `initialize_colors()`, `aggregate_colors()` and `pool_colors()`.
        * `initialize_colors()` should store the initialized colors in 
        `self.color` as a numpy array. 
        * `aggregate_colors()` should return a numpy array storing the result
        of color aggregation. It will be then sorted and only the rank will
        be kept as the updated colors. Notice that this method can return an
        array with **ANY** element type; even `object`-arrays are okay.
        * `pool_colors()` should take the stable coloring as input, and return 
        the representation of the graph.
    """
    def __init__(self):
        self.color: np.ndarray

    def initialize_colors(self, *args, **kwargs):
        """
        Define the rule to initialize colors. Usage of external information
        is allowed, by passing arguments to this method.
        """
        raise NotImplementedError()
    
    def aggregate_colors(self) -> np.ndarray:
        """
        Define the rule to aggregate colors.
        """
        raise NotImplementedError()
    
    def pool_colors(self, coloring) -> MultiSet:
        """
        Define the rule to pool colors into a representation of the graph.
        """
        raise NotImplementedError()

    def update_colors(self):
        color_list = self.aggregate_colors()
        self.color = (rankdata(color_list, method='dense') - 1).astype(np.int64)

    def set_graph(self, graph, 
                  format: Literal['adj', 'dense', 'sparse'] = 'adj'):
        if format == 'adj':
            self.graph: AdjList = graph
        elif format == 'dense':
            self.graph = AdjList.from_dense_adj(graph)
        elif format == 'sparse':
            self.graph = AdjList.from_sparse_adj(graph)
        
        for i in range(self.graph.num_nodes):
            if i not in self.graph.adj_dict:
                self.graph.adj_dict[i] = set()

    def update_colors_test_stable(self):
        """
        Call `update_colors()` and test whether a stable coloring has been
        reached.
        """
        old_color = self.color
        self.update_colors()
        if np.all(old_color == self.color):
            return True
        return False
    
    def get_stable_coloring(self):
        while not self.update_colors_test_stable(): pass
        return self.aggregate_colors()
        
    def representation(self) -> MultiSet:
        """
        Return the multiset of stable coloring.
        """
        return self.pool_colors(self.get_stable_coloring())
