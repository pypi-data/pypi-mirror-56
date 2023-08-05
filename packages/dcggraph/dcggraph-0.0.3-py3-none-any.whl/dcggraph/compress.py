"""
This file contains predicated DCG compression: which is essentially flattening
nodes that fail a predicate in a Directed Cyclic Graph. The result is a
graph where all the nodes pass the predicate.
"""

from typing import Union, List, Callable, Dict, Text
from enum import Enum
from collections import deque

from dcggraph import DCGnode, DCGgraph
from dcggraph.search import DCGsearch

class DCGcompress:
    # pylint: disable=R0902,R0903
    """
    DCG compression is essentially flattening nodes that fail a predicate in 
    a Directed Cyclic Graph. The result is a graph where all the nodes pass 
    the predicate. This function is build upon the dcggraph.search function.

    """
    def __init__(self, graph: DCGgraph,
                 predicate: PredicateFunc = None) -> None:
        """
        The graph is needed to make sure the nodes we are working with are
        actually in the graph.
        The predicate is optional, and defaults to a reachability search
        (meaning, disjoint nodes, or directionally upstream nodes will not
        be returned).
        """
        self._graph = graph
        if predicate is None:
            predicate = DCGsearch.default_predicate
        self._predicate = predicate
        self._memo = {}
        # these are reset during each search
        self._tovisit = deque([])
        self._visited = {}
        self._passed = {}
        self._failed = {}
        self._unresolved = {}

    @staticmethod
    def default_predicate(node: DCGnode,
                          visited: DCGnodeVisitedHash,
                          passed: DCGnodePassedHash,
                          failed: DCGnodeFailedHash) -> PredicateResult:
        """
        create a default predicate to keep the rest of the code simple
        the default predicate simply does a graph reachability search
        """
        # pylint: disable=W0613
        return PredicateResult.PASS

    def more_to_visit(self) -> DCGnode:
        """returns the next node to visit"""
        return len(self._tovisit) > 0

    def get_next_to_visit(self) -> DCGnode:
        """returns the next node to visit"""
        return self._tovisit.popleft()

    def set_next_to_visit(self, node: DCGnode) -> None:
        """
        puts the node on the top of the stack to visit next if
        it is not already visited
        """
        if node.name not in self._visited:
            self._visited[node.name] = True
            self._tovisit.appendleft(node)

    def set_passed(self, node: DCGnode) -> None:
        """
        marks the node as passing the predicate, and removes it
        from the failed and unresolved lists
        """
        self._passed[node.name] = node
        self._memo[node.name] = True
        if node.name in self._failed:
            self._failed.pop(node.name)
        if node.name in self._unresolved:
            self._unresolved.pop(node.name)

    @property
    def all_passed(self):
        """returns all passed nodes in the current search"""
        return self._passed.values()

    def set_failed(self, node: DCGnode) -> None:
        """
        marks the node as failing the predicate, and removes it
        from the passing and unresolved lists
        """
        self._failed[node.name] = node
        self._memo[node.name] = False
        if node.name in self._passed:
            self._passed.pop(node.name)
        if node.name in self._unresolved:
            self._unresolved.pop(node.name)

    @property
    def all_failed(self):
        """returns all failed nodes in the current search"""
        return self._failed.values()

    def set_unresolved(self, node: DCGnode) -> None:
        """
        marks the node as unresolved after the predicate, and removes it
        from the passing and failing lists (and the memo!)
        """
        self._unresolved[node.name] = node
        if node.name in self._memo:
            self._memo.pop(node.name)
        if node.name in self._passed:
            self._passed.pop(node.name)
        if node.name in self._failed:
            self._failed.pop(node.name)

    @property
    def all_unresolved(self):
        """returns all unresolved nodes in the current search"""
        return self._unresolved.values()

    def reset_search(self) -> None:
        """resets an individual-search state (but not the memo)"""
        self._tovisit = deque([])
        self._visited = {}
        self._passed = {}
        self._failed = {}
        self._unresolved = {}

    def recheck_predicates(self) -> None:
        """
        re-evaluate predicates for all unresolved nodes after another
        nodes has been placed in passed/failed.
        """
        recheck = True
        while recheck:
            recheck = False
            for node in list(self.all_unresolved):
                res = self._predicate(node, self._visited,
                                      self._passed, self._failed)
                if res == PredicateResult.PASS:
                    self.set_passed(node)
                    recheck = True
                elif res == PredicateResult.FAIL:
                    self.set_failed(node)
                    recheck = True
                elif res == PredicateResult.WAIT:
                    pass
                else:
                    raise Exception(f"invalid return status {res}")

    def check_predicate(self, node: DCGnode) -> None:
        """
        checks if the node passes the predicate or is already passed
        in the memo. If the node conclusively passes or fails, the
        any unresolved nodes are re-checked. If the predicate marks this
        node as unresolved, it will go in the unresolved queue
        """
        if node.name in self._memo:
            if self._memo[node.name]:
                self.set_passed(node)
            else:
                self.set_failed(node)
        else:
            res = self._predicate(node, self._visited,
                                  self._passed, self._failed)
            if res == PredicateResult.PASS:
                self.set_passed(node)
            elif res == PredicateResult.FAIL:
                self.set_failed(node)
            elif res == PredicateResult.WAIT:
                self.set_unresolved(node)
            else:
                raise Exception(f"invalid return status {res}")
        self.recheck_predicates()

    def search(self, start_node: Union[DCGnode, Text]) -> List[DCGnode]:
        """
        returns all nodes in graph reachable from this node. Reachable means
        that the node is physically reachable and also passes the predicate
        test. If by the end of the search, the node state is still unresolved,
        it will be marked as failed.
        """
        # initialize state (make sure the node is in the graph)
        self.reset_search()
        if isinstance(start_node, DCGnode):
            self.set_next_to_visit(self._graph.get_node(start_node.name))
        else:
            self.set_next_to_visit(self._graph.get_node(start_node))

        # search through all the reachable nodes, checking against predicate
        while self.more_to_visit():
            node = self.get_next_to_visit()
            self.check_predicate(node)
            for edge in node.edges_out:
                self.set_next_to_visit(edge.to_node)

        # at this point, any unresolved nodes will never pass. so fail them
        for node in list(self.all_unresolved):
            self.set_failed(node)

        return self.all_passed
