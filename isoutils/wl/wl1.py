import numpy as np
from ..utils import MultiSet
from .base import BaseWL
from typing import Optional

class WL1(BaseWL):
    """
    WL1 solver.
    """
    def __init__(self):
        super().__init__()
    
    def initialize_colors(self, precolor: Optional[np.ndarray] = None):
        if precolor is not None:
            self.color = precolor
        else:
            self.color = np.zeros((self.graph.num_nodes, ), dtype=np.int64)

    def aggregate_colors(self):
        color_list = np.zeros((self.graph.num_nodes, ), dtype=object)
        for node in range(self.graph.num_nodes):
            color_list[node] = tuple(np.concatenate(
                [np.array([self.color[node]], dtype=np.int64),
                 np.sort(self.color[list(self.graph.adj_dict[node])])]
            ))
        return color_list
    
    def pool_colors(self, coloring) -> MultiSet:
        return MultiSet.from_iterable(coloring)
