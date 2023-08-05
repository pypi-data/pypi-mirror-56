Directed Cyclic Graph Utilities for Python
==========================================

This package currently used for doing predicated searches from a given 
node in a directed graph that is allowed to be cyclic. Some points to clear
up confusion:
- __directed__: means an edge between 2 nodes can only be travelled in one 
  direction
- __predicated__: means that even if a node is reachable, it still has to
  pass a prediate test (i.e. `predicate(node) == True`) in order to be 
  returned.
    - this means there are really 2 search filters in the graph:
        1) the node has to be reachable without any filtering
        2) the node has to pass the predicate test
- __cyclic__: means that if you start from a node, and follow a bunch of 
  paths, you can end up at the same node. This makes things a lot harder
  than if you were working with DAGs.

API
---
TODO. but for now, just look at the tests to see how to run searches

installing
----------
TODO. but eventually put on pypi

