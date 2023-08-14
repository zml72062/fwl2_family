import numpy as np
from isoutils.furer import get_furer_graph_pair_with_precolor
from isoutils.comparer import wl_test

name = ['3-clique', # sanity check
        '4-clique', # sanity check
        'figure 4',
        'figure 5',
        'figure 6',
        'figure 7',
        'figure 8',
        'figure 9',
        'figure 10',
        'figure 11',]

base_graph = [[[0, 1, 1, 2, 2, 0],
               [1, 0, 2, 1, 0, 2]],
               # 3-clique, give rise to 6-cycle vs 2 * 3-cycle
              [[0, 1, 1, 2, 2, 3, 3, 0, 1, 3, 0, 2], 
               [1, 0, 2, 1, 3, 2, 0, 3, 3, 1, 2, 0]], 
               # 4-clique, give rise to shrikhande vs 4x4-rook
              [[0, 1, 1, 2, 2, 0, 1, 3, 2, 3, 3, 4, 4, 5, 3, 5, 4, 6, 5, 6], 
               [1, 0, 2, 1, 0, 2, 3, 1, 3, 2, 4, 3, 5, 4, 5, 3, 6, 4, 6, 5]],
               # figure 4 of SWL paper
              [[0, 1, 1, 2, 2, 0, 0, 3, 0, 4, 3, 4, 3, 7, 4, 7, 5, 6, 6, 7, 5, 7], 
               [1, 0, 2, 1, 0, 2, 3, 0, 4, 0, 4, 3, 7, 3, 7, 4, 6, 5, 7, 6, 7, 5]], 
               # figure 5 of SWL paper
              [[0, 1, 1, 2, 2, 0, 1, 3, 2, 3, 3, 4, 4, 5, 5, 3, 5, 6, 6, 7, 7, 5, 6, 8, 7, 8], 
               [1, 0, 2, 1, 0, 2, 3, 1, 3, 2, 4, 3, 5, 4, 3, 5, 6, 5, 7, 6, 5, 7, 8, 6, 8, 7]], 
               # figure 6 of SWL paper
              [[0, 1, 0, 2, 1, 3, 2, 3, 2, 4, 4, 5, 5, 3, 4, 6, 6, 7, 7, 5], 
               [1, 0, 2, 0, 3, 1, 3, 2, 4, 2, 5, 4, 3, 5, 6, 4, 7, 6, 5, 7]],
               # figure 7 of SWL paper
              [[0, 1, 1, 2, 2, 0, 1, 3, 3, 4, 4, 1, 2, 4, 4, 5, 5, 2], 
               [1, 0, 2, 1, 0, 2, 3, 1, 4, 3, 1, 4, 4, 2, 5, 4, 2, 5]],
               # figure 8 of SWL paper
              [[0, 1, 1, 3, 3, 5, 5, 4, 4, 2, 2, 0, 0, 6, 6, 4, 1, 7, 7, 5], 
               [1, 0, 3, 1, 5, 3, 4, 5, 2, 4, 0, 2, 6, 0, 4, 6, 7, 1, 5, 7]],
               # figure 9 of SWL paper
              [[0, 3, 3, 1, 1, 7, 7, 2, 2, 5, 5, 0, 0, 4, 4, 1, 1, 8, 8, 2, 2, 6, 6, 0],
               [3, 0, 1, 3, 7, 1, 2, 7, 5, 2, 0, 5, 4, 0, 1, 4, 8, 1, 2, 8, 6, 2, 0, 6]],
               # figure 10 of SWL paper
              [[0, 2, 2, 5, 5, 7, 7, 8, 8, 11, 11, 14, 14, 12, 12, 9, 9, 7, 7, 6, 6, 3, 3, 0, 0, 1, 1, 5, 8, 10, 10, 14, 14, 13, 13, 9, 0, 4, 4, 6],
               [2, 0, 5, 2, 7, 5, 8, 7, 11, 8, 14, 11, 12, 14, 9, 12, 7, 9, 6, 7, 3, 6, 0, 3, 1, 0, 5, 1, 10, 8, 14, 10, 13, 14, 9, 13, 4, 0, 6, 4]],
               # figure 11 of SWL paper
]

print(f"On box graph:") # another sanity check
G_base, H_base, _, _ = get_furer_graph_pair_with_precolor(
    np.array(base_graph[0], dtype=np.int64)
)
G = np.concatenate([G_base, H_base + 6, G_base + 12, H_base + 18,
 np.stack([np.arange(0, 6, dtype=np.int64), np.full((6, ), 24, dtype=np.int64)]),
 np.stack([np.arange(6, 12, dtype=np.int64), np.full((6, ), 25, dtype=np.int64)]),
 np.stack([np.arange(12, 18, dtype=np.int64), np.full((6, ), 26, dtype=np.int64)]),
 np.stack([np.arange(18, 24, dtype=np.int64), np.full((6, ), 27, dtype=np.int64)]),
 np.stack([np.full((6, ), 24, dtype=np.int64), np.arange(0, 6, dtype=np.int64)]),
 np.stack([np.full((6, ), 25, dtype=np.int64), np.arange(6, 12, dtype=np.int64)]),
 np.stack([np.full((6, ), 26, dtype=np.int64), np.arange(12, 18, dtype=np.int64)]),
 np.stack([np.full((6, ), 27, dtype=np.int64), np.arange(18, 24, dtype=np.int64)]),
 np.array(
     [[24, 25, 25, 26, 26, 27, 27, 24],
      [25, 24, 26, 25, 27, 26, 24, 27]], dtype=np.int64
 )], axis=1
)
H = np.concatenate([G_base, G_base + 6, H_base + 12, H_base + 18,
 np.stack([np.arange(0, 6, dtype=np.int64), np.full((6, ), 24, dtype=np.int64)]),
 np.stack([np.arange(6, 12, dtype=np.int64), np.full((6, ), 25, dtype=np.int64)]),
 np.stack([np.arange(12, 18, dtype=np.int64), np.full((6, ), 26, dtype=np.int64)]),
 np.stack([np.arange(18, 24, dtype=np.int64), np.full((6, ), 27, dtype=np.int64)]),
 np.stack([np.full((6, ), 24, dtype=np.int64), np.arange(0, 6, dtype=np.int64)]),
 np.stack([np.full((6, ), 25, dtype=np.int64), np.arange(6, 12, dtype=np.int64)]),
 np.stack([np.full((6, ), 26, dtype=np.int64), np.arange(12, 18, dtype=np.int64)]),
 np.stack([np.full((6, ), 27, dtype=np.int64), np.arange(18, 24, dtype=np.int64)]),
 np.array(
     [[24, 25, 25, 26, 26, 27, 27, 24],
      [25, 24, 26, 25, 27, 26, 24, 27]], dtype=np.int64
 )], axis=1
)
G_precolor, H_precolor = np.array([0] * 24 + [1] * 4, dtype=np.int64
                      ), np.array([0] * 24 + [1] * 4, dtype=np.int64)
for method in ['WL2', 'FWL2', 'LFWL', 'SLFWL', 'SWL_SV', 'SWL_VS',
                    'SWL_SV_P', 'SWL_VS_P', 'SWL_SV_G', 'SWL_VS_G',
                    'PSWL_SV', 'PSWL_VS', 'GSWL_SV', 'GSWL_VS',
                    'GSWL_SV_P', 'GSWL_VS_P', 'SSWL_SV', 'SSWL_VS',
                    'FullSWL_SV', 'FullSWL_VS']:
    print(f"{method} {'can' if wl_test(method, G, H, G_precolor, H_precolor) else 'cannot'} discriminate b/w G & H.")


for n, base in zip(name, base_graph):
    G, H, G_precolor, H_precolor = get_furer_graph_pair_with_precolor(
        np.array(base, dtype=np.int64)
    )
    print(f"On {n}:")
    for method in ['WL2', 'FWL2', 'LFWL', 'SLFWL', 'SWL_SV', 'SWL_VS',
                        'SWL_SV_P', 'SWL_VS_P', 'SWL_SV_G', 'SWL_VS_G',
                        'PSWL_SV', 'PSWL_VS', 'GSWL_SV', 'GSWL_VS',
                        'GSWL_SV_P', 'GSWL_VS_P', 'SSWL_SV', 'SSWL_VS',
                        'FullSWL_SV', 'FullSWL_VS']:
        print(f"{method} {'can' if wl_test(method, G, H, G_precolor, H_precolor) else 'cannot'} discriminate b/w G & H.")

