"""
This file contains everything related to predicated search functionality
"""
from typing import Union, List, Callable, Dict, Text
from enum import Enum
from collections import deque

from dcggraph import DCGnode, DCGgraph

class PredicateResult(Enum):
    """
    PASS means the node should be returned in the search results
    FAIL means the node should not be returned in the search results
    WAIT means we will defer the decision to PASS/FAIL until we have more
         information (typical in cyclic graphs, where traversal order
         matters). NOTE: we may never get all the information we need by
         the end of the search, which is an implicit FAIL!
    """
    PASS = 1
    FAIL = 2
    WAIT = 3

# These are the various signatures for the user-supplied prediate function
DCGnodeVisitedHash = Dict[Text, DCGnode]
DCGnodePassedHash = Dict[Text, DCGnode]
DCGnodeFailedHash = Dict[Text, DCGnode]
PredicateFunc = Callable[[DCGnode, DCGnodeVisitedHash, DCGnodePassedHash,
                          DCGnodeFailedHash], PredicateResult]

class DCGsearch:
    # pylint: disable=R0902,R0903
    """
    The DCGsearch object stores a memo of search results, so you can call
    the same search from multiple nodes in the graph, and the results
    from visited nodes in previous searches will be available to later
    searches.

    IMPORTANT NOTE: the memo assumes that once a node is asserted PASS/FAIL,
    it will never resolve to any other answer. If you expect your nodes
    to have dynamically changing predicate results for each search, you
    should just create a new DCGsearch object for each search, instead of
    reusing the existing one... since a main objective of DCGsearch is to
    cache PASS/FAIL results between searches for each node
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

    @property
    def graph(self) -> DCGgraph:
        """returns the underlying graph"""
        return self._graph

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
            self.set_next_to_visit(self.graph.get_node(start_node.name))
        else:
            self.set_next_to_visit(self.graph.get_node(start_node))

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

    def compress(self) -> "DCGsearch":
        """
        Compression is effectively removing any nodes that fail the predicate,
        and merging the input and output edges. This means The resulting
        graph is composed only of nodes that pass the predicate. This function
        internally calls search() for each node. After compression, any
        node.edges_out will be sure to lead to a node that passes a predicate

        This will return a brand new DCGsearch based on the compressed graph
        and the predicate will simply be a reachability search
        """
        keep_nodes = {}
        new_edges = {}

        # 1) run search for every node, and keep track of all passing
        for node in self.graph.nodes:
            for keep_node in self.search(node):
                keep_nodes[keep_node.name] = keep_node

        # 2) remove all failing nodes, and outer-product the in/out edges
        #    to make new edges in the new graph
        for node in keep_nodes.values():
            new_edges[node.name] = {}
            edges_to_visit = deque(node.edges_out)
            while len(edges_to_visit) > 0:
                edge = edges_to_visit.popleft()
                if edge.to_node.name not in keep_nodes:
                    edges_to_visit.extend(edge.to_node.edges_out)
                else:
                    new_edges[node.name][edge.to_node.name] = True

        # 3) add the passing nodes and the new edges to the compressed graph
        new_graph = DCGgraph()
        for node_name in keep_nodes:
            new_graph.create_node(node_name)
        for from_node_name, to_node_names in new_edges.items():
            from_node = new_graph.get_node(from_node_name)
            for to_node_name in to_node_names.keys():
                to_node = new_graph.get_node(to_node_name)
                new_graph.create_edge(from_node, to_node)

        # use default predicate in new graph
        return DCGsearch(new_graph)
