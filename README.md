# Verifying the hierarchy within FWL(2) family

This repository aims at verifying the expressiveness hierarchy proposed in [A Complete Expressiveness Hierarchy for Subgraph GNNs via Subgraph Weisfeiler-Lehman Tests](https://arxiv.org/pdf/2302.07090.pdf).

To achieve this goal, two independent modules are developed:
* `isoutils.furer`: building generalized Fürer graph from arbitrary base graph
* `isoutils.wl`: support for any isomorphism test within the FWL(2) family

## Tests

Running `python strongly_regular.py` should produce two `True`. This script builds 4x4 Rook's graph and Shrikhande graph from definition, and compare them with the generalized Fürer graph constructed from a 4-clique.

To produce results for the [paper](https://arxiv.org/pdf/2302.07090.pdf), run `python examples.py`.