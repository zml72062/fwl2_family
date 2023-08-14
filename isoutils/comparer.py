import numpy as np
from .wl import *
from typing import Optional, Callable

def method_resolve(method: str) -> Callable:
    assert method in {'WL2', 'FWL2', 'LFWL', 'SLFWL', 'SWL_SV', 'SWL_VS',
                      'SWL_SV_P', 'SWL_VS_P', 'SWL_SV_G', 'SWL_VS_G',
                      'PSWL_SV', 'PSWL_VS', 'GSWL_SV', 'GSWL_VS',
                      'GSWL_SV_P', 'GSWL_VS_P', 'SSWL_SV', 'SSWL_VS',
                      'FullSWL_SV', 'FullSWL_VS', 'WL1'}, "Invalid method!"
    return eval(method)

def wl_test(method: str, G: np.ndarray, H: np.ndarray,
            G_precolor: Optional[np.ndarray] = None, 
            H_precolor: Optional[np.ndarray] = None) -> bool:
    solver: BaseWL = method_resolve(method)()
    solver.set_graph(G, 'sparse')
    if method != 'WL1':
        solver.initialize_colors(identity=True, precolor=G_precolor)
    else:
        solver.initialize_colors(precolor=G_precolor)
    G_multiset = solver.representation()

    solver.set_graph(H, 'sparse')
    if method != 'WL1':
        solver.initialize_colors(identity=True, precolor=H_precolor)
    else:
        solver.initialize_colors(precolor=H_precolor)
    H_multiset = solver.representation()

    return G_multiset != H_multiset

