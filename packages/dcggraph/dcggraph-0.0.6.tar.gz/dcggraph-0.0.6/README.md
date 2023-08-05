Directed Cyclic Graph Utilities for Python
==========================================

installing
----------
```pip install dcggraph```

description
-----------
This package currently used for doing predicated searches from a given
node in a directed graph that is allowed to be cyclic. Some points to clear
up confusion:
- __directed__: means an edge between 2 nodes can only be travelled in one
  direction _(although there can be two edges going opposite directions between the same two nodes)
- __predicated__: means that even if a node is reachable, it still has to
  pass a prediate test (i.e. `predicate(node) == True`) in order to be
  returned.
    - this means there are really 2 search filters in the graph:
        1) the node has to be reachable without any filtering
        2) the node has to pass the predicate test
- __cyclic__: means that if you start from a node, and follow a bunch of
  paths, you can end up at the same node. This makes things a lot harder
  than if you were working with DAGs.

cycles are tricky
-----------------
The main trick used to deal with cycles is having the predicate return 3 states:
  1) `PASS`: means the node confidently passes the predicate
  2) `FAIL`: means the node confidently fails the predicate
  3) `WAIT`: means the node is unsure if it passes yet, and would like to defer giving a
     confident answer until more nodes are seen (since starting point matters in cyclical graphs)
     
Nodes that return the `WAIT` state from a predicate get put in the `unresolved` list, and are re-evaluated every time another node returns `PASS` or `FAIL`.  After all reachable nodes have been evaluated, any remaining nodes in the `unresolved` list are demoted to the `FAIL` state, since they couldn't make up their mind, and there are no more chances for them to give a real answer.

This algorithm seems to work well for the cases I use predicated searches in a graph. I'm __positive__ better algorithms exist than what is implemented here.

API
---
The main feature is predicated graph compression and search. 
In addition to the snippet below, look at the tests for example usage
```python
import re
from dcggraph import DCGnode, DCGedge, DCGgraph
from dcggraph.search import PredicateResult, DCGsearch

g = DCGgraph()
n0 = g.create_node("n0")
n1 = g.create_node("n1")
n2 = g.create_node("n2")
n3 = g.create_node("n3")
n4 = g.create_node("n4")
g.create_edge(n0, n1)
g.create_edge(n0, n2)
g.create_edge(n1, n3)
g.create_edge(n1, n4)

def even(node, visited, passed, failed):
   if f re.match("[a-z][02468]", node.name):
       return PredicateResult.PASS
   else:
       return PredicateResult.FAIL

s1 = DCGsearch(g, even)

# reuse the search object to cache FAIL/PASS results between searches
assertEqual(len(s1.search(n0)), 3)
assertEqual(len(s1.search(n1)), 1)
assertEqual(len(s1.search(n2)), 1)
assertEqual(len(s1.search(n3)), 0)
assertEqual(len(s1.search(n4)), 1)

```

