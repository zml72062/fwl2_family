import numpy as np
from .base import BaseWL
from ..utils import MultiSet, FrozenMultiSet
from typing import Optional
from scipy.stats import rankdata

class WL2Base(BaseWL):
    """
    Base solver for all WL(2)/FWL(2)-type algorithms.
    """
    def __init__(self):
        super().__init__()

    def to2d(self, A: np.ndarray) -> np.ndarray:
        return A.reshape((self.graph.num_nodes, self.graph.num_nodes))

    def initialize_colors(self, identity: bool = False,
                          precolor: Optional[np.ndarray] = None):
        """
        Set `identity=True` if one wants identity marking.
        """
        self.color = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        dense_adj = self.graph.to_dense_adj()
        for i in range(self.graph.num_nodes):
            for j in range(self.graph.num_nodes):
                color_ij = [dense_adj[i, j]]
                if identity:
                    color_ij.append(i == j)
                if precolor is not None:
                    color_ij += [precolor[i], precolor[j]]
                self.color[i, j] = tuple(color_ij)
        
        self.color = self.color.reshape(-1)
        self.color = (rankdata(self.color, method='dense') - 1).astype(np.int64)

    def aggregate_colors(self):
        raise NotImplementedError()
    
    def pool_colors(self, coloring) -> MultiSet:
        raise NotImplementedError()
    
    """
    Below, we implement all operations defined in the paper "A Complete 
    Expressiveness Hierarchy for Subgraph GNNs via Subgraph Weisfeiler-
    Lehman Tests".
    """
    def global_u(self) -> np.ndarray:
        """
        \sum_(w \in V) h(u, w) -> h(u, v)
        """
        old_color = self.to2d(self.color)
        color_list = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        for node in range(self.graph.num_nodes):
            for _ in range(self.graph.num_nodes):
                color_list[node, _] = tuple(np.sort(old_color[node, :]))
        
        return color_list.reshape(-1)
    
    def global_v(self) -> np.ndarray:
        """
        \sum_(w \in V) h(w, v) -> h(u, v)
        """
        old_color = self.to2d(self.color)
        color_list = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        for _ in range(self.graph.num_nodes):
            for node in range(self.graph.num_nodes):
                color_list[_, node] = tuple(np.sort(old_color[:, node]))
        
        return color_list.reshape(-1)
    
    def local_u(self) -> np.ndarray:
        """
        \sum_(w \in N(v)) h(u, w) -> h(u, v)
        """
        old_color = self.to2d(self.color)
        color_list = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        for node in range(self.graph.num_nodes):
            for central in range(self.graph.num_nodes):
                color_list[node, central] = tuple(
                    np.sort(old_color[node, list(self.graph.adj_dict[central])])
                )
        
        return color_list.reshape(-1)
    
    def local_v(self) -> np.ndarray:
        """
        \sum_(w \in N(u)) h(w, v) -> h(u, v)
        """
        old_color = self.to2d(self.color)
        color_list = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        for central in range(self.graph.num_nodes):
            for node in range(self.graph.num_nodes):
                color_list[central, node] = tuple(
                    np.sort(old_color[list(self.graph.adj_dict[central]), node])
                )
        
        return color_list.reshape(-1)
    
    def pointwise_uv(self) -> np.ndarray:
        """
        h(u, v) -> h(u, v)
        """
        return self.color.astype(object)
    
    def pointwise_vu(self) -> np.ndarray:
        """
        h(v, u) -> h(u, v)
        """
        return self.to2d(self.color).T.reshape(-1).astype(object)
    
    def pointwise_uu(self) -> np.ndarray:
        """
        h(u, u) -> h(u, v)
        """
        old_color = self.to2d(self.color)
        return np.broadcast_to(np.diagonal(old_color)[:, None],
                               old_color.shape).reshape(-1).astype(object)
    
    def pointwise_vv(self) -> np.ndarray:
        """
        h(v, v) -> h(u, v)
        """
        old_color = self.to2d(self.color)
        return np.broadcast_to(np.diagonal(old_color)[None, :],
                               old_color.shape).reshape(-1).astype(object)
    
    def global_fwl2(self) -> np.ndarray:
        """
        \sum_(w \in V) (h(u, w), h(w, v)) -> h(u, v)
        """
        color_list = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        old_color = self.to2d(self.color)

        for i in range(self.graph.num_nodes):
            for j in range(self.graph.num_nodes):
                color_ij = np.zeros((self.graph.num_nodes, ), dtype=object)
                for k in range(self.graph.num_nodes):
                    color_ij[k] = (old_color[i, k], old_color[k, j])
                color_list[i, j] = tuple(np.sort(color_ij))

        return color_list.reshape(-1)
    
    def local_u_fwl2(self) -> np.ndarray:
        """
        \sum_(w \in N(u)) (h(u, w), h(w, v)) -> h(u, v)
        """
        color_list = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        old_color = self.to2d(self.color)
        
        for i in range(self.graph.num_nodes):
            for j in range(self.graph.num_nodes):
                adj_list = list(self.graph.adj_dict[i])
                color_ij = np.zeros((len(adj_list), ), dtype=object)
                for k_idx, k in enumerate(adj_list):
                    color_ij[k_idx] = (old_color[i, k], old_color[k, j])
                color_list[i, j] = tuple(np.sort(color_ij))

        return color_list.reshape(-1)
    
    def local_v_fwl2(self) -> np.ndarray:
        """
        \sum_(w \in N(v)) (h(u, w), h(w, v)) -> h(u, v)
        """
        color_list = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        old_color = self.to2d(self.color)

        for i in range(self.graph.num_nodes):
            for j in range(self.graph.num_nodes):
                adj_list = list(self.graph.adj_dict[j])
                color_ij = np.zeros((len(adj_list), ), dtype=object)
                for k_idx, k in enumerate(adj_list):
                    color_ij[k_idx] = (old_color[i, k], old_color[k, j])
                color_list[i, j] = tuple(np.sort(color_ij))

        return color_list.reshape(-1)
    
    def local_uv_fwl2(self) -> np.ndarray:
        """
        \sum_(w \in N(u) or N(v)) (h(u, w), h(w, v)) -> h(u, v)
        """
        color_list = np.zeros((self.graph.num_nodes, self.graph.num_nodes),
                              dtype=object)
        old_color = self.to2d(self.color)

        for i in range(self.graph.num_nodes):
            for j in range(self.graph.num_nodes):
                adj_list = list(self.graph.adj_dict[i] | self.graph.adj_dict[j])
                color_ij = np.zeros((len(adj_list), ), dtype=object)
                for k_idx, k in enumerate(adj_list):
                    color_ij[k_idx] = (old_color[i, k], old_color[k, j])
                color_list[i, j] = tuple(np.sort(color_ij))

        return color_list.reshape(-1)

    def color_concat(self, *colors) -> np.ndarray:
        """
        Concat multiple colors into one.
        """
        color_list = np.zeros((self.graph.num_nodes ** 2, ), dtype=object)

        for i in range(self.graph.num_nodes ** 2):
            color_list[i] = tuple((color[i] for color in colors))
        
        return color_list
    
    def pool_vs(self, coloring) -> MultiSet:
        return MultiSet.from_iterable(
            (FrozenMultiSet.from_iterable(row) for row in self.to2d(coloring))
        )
    
    def pool_sv(self, coloring) -> MultiSet:
        return MultiSet.from_iterable(
            (FrozenMultiSet.from_iterable(row) for row in self.to2d(coloring).T)
        )
    
    def pool_all(self, coloring) -> MultiSet:
        return MultiSet.from_iterable(coloring)
    
        