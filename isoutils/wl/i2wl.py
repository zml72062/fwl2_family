import numpy as np
from ..utils import MultiSet, FrozenMultiSet
from .base import BaseWL
from typing import Literal, Optional
from scipy.stats import rankdata

class I2WL(BaseWL):
    def __init__(self):
        super().__init__()
    
    def set_graph(self, graph, format: Literal['adj', 'dense', 'sparse'] = 'adj'):
        super().set_graph(graph, format)
        if format == 'sparse':
            self.edge_index = graph
        else:
            raise RuntimeError('Unsupported graph format!')

    def initialize_colors(self, identity: bool = True,
                          precolor: Optional[np.ndarray] = None):
        self.color = np.zeros((self.graph.num_edges, self.graph.num_nodes),
                              dtype=object)
        for e_i, (i, j) in enumerate(self.edge_index.T):
            for k in range(self.graph.num_nodes):
                if identity:
                    if k == i or k == j:
                        color_e_i_k = [1]
                    else:
                        color_e_i_k = [0]
                else:
                    color_e_i_k = [0]
                
                if precolor is not None:
                    color_e_i_k += [precolor[i], precolor[j], precolor[k]]
                self.color[e_i][k] = tuple(color_e_i_k)
            
        self.color = self.color.reshape(-1)
        self.color = (rankdata(self.color, method='dense') - 1).astype(np.int64)

    def aggregate_colors(self):
        color_list = np.zeros((self.graph.num_edges, self.graph.num_nodes), 
                              dtype=object)
        for e_i in range(self.graph.num_edges):
            for node in range(self.graph.num_nodes):
                color_list[e_i][node] = tuple(np.concatenate(
                    [np.array([self.color.reshape(-1, self.graph.num_nodes)[e_i][node]], dtype=np.int64),
                     np.sort(self.color.reshape(-1, self.graph.num_nodes)[e_i][list(self.graph.adj_dict[node])])]
                ))
        return color_list
    
    def pool_colors(self, coloring):
        return MultiSet.from_iterable(
            [FrozenMultiSet.from_iterable(row) for row in coloring.reshape(-1, self.graph.num_nodes)]
        )


        
