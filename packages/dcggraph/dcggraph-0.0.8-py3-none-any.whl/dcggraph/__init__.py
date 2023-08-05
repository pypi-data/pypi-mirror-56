"""
This file contains the base classes for the dcggraph package.
"""

from collections import deque
from typing import Set, Text

class DCGnode:
    """A node in the DCG"""
    def __init__(self, name):
        self._name = name
        self._edges_out = {}
        self._edges_in = {}

    def __repr__(self):
        return f"DCGnode({self.name})"

    def __eq__(self, other):
        return self.name == other.name

    def clone(self)-> "DCGnode":
        """returns a clone of this node WITHOUT ANY EDGES"""
        return DCGnode(self.name)

    @property
    def name(self)->str:
        """returns the node name"""
        return self._name

    @property
    def root(self) -> bool:
        """if this node has no edges-in"""
        return len(self._edges_in) == 0

    def edge_in_by_node(self, name: str) -> "DCGedge":
        """returns the edge_in by the given from_node"""
        matches = list(filter(lambda e: e.from_node.name == name,
                              self._edges_in.values()))
        if len(matches) != 1:
            raise Exception(f"{self} has no edge_in with from_node={name}")
        return matches[0]

    @property
    def edges_in(self) -> Set["DCGedge"]:
        """returns the UNSORTED set of edges pointing in to this node"""
        return list(self._edges_in.values())

    def add_edge_in(self, edge: "DCGedge") -> None:
        """adds an inward-pointing edge"""
        if edge.name in self._edges_in:
            raise Exception(f"{edge} is already connected to {self}")
        if edge.to_node != self:
            raise Exception(f"{edge} is not connected to {self}")
        self._edges_in[edge.name] = edge

    def edge_out_by_node(self, name: str) -> "DCGedge":
        """returns the edge_in by the given to_node"""
        matches = list(filter(lambda e: e.to_node.name == name,
                              self._edges_out.values()))
        if len(matches) != 1:
            raise Exception(f"{self} has no edge_out with to_node={name}")
        return matches[0]


    @property
    def edges_out(self) -> Set["DCGedge"]:
        """returns the UNSORTED set of edges out of this node"""
        return list(self._edges_out.values())

    def add_edge_out(self, edge: "DCGedge") -> None:
        """adds an outward-pointing edge"""
        if edge.name in self._edges_out:
            raise Exception(f"{edge} is already connected from {self}")
        if edge.from_node != self:
            raise Exception(f"{edge} is not connected from {self}")
        self._edges_out[edge.name] = edge

    def deep_equal(self, other: "DCGnode") -> bool:
        """do a deep comparison of every node in the hierarchy"""
        visited = {}
        tovisit = deque([(self, other)])
        while len(tovisit) > 0:
            (snode, onode) = tovisit.popleft()
            if snode.name in visited:
                continue
            visited[snode.name] = True
            if snode != onode:
                return False

            snodes_out = list(map(lambda e: e.to_node, snode.edges_out))
            onodes_out = list(map(lambda e: e.to_node, onode.edges_out))
            if len(snodes_out) != len(onodes_out):
                return False

            tovisit.extend(zip(snodes_out, onodes_out))
        return True

class DCGedge:
    """An non-weighted, directed edge in the DCG"""
    def __init__(self, name: str, from_node: DCGnode,
                 to_node: DCGnode) -> None:
        self._name = name
        self._from_node = from_node
        self._to_node = to_node

    def __repr__(self):
        return f"DCGedge({self.from_node},{self.to_node})"

    def __eq__(self, other):
        """determine edge equality based on from/to nodes only"""
        return (self.from_node.name == other.from_node.name) and \
               (self.to_node.name == other.to_node.name)

    @property
    def name(self)->Text:
        """returns the name of this edge"""
        return self._name

    @property
    def from_node(self)->DCGnode:
        """returns the source node"""
        return self._from_node

    @property
    def to_node(self)->DCGnode:
        """returns the dest node"""
        return self._to_node

class DCGgraph:
    """
    A minimal-feature Directed-Cyclic-Graph used mainly for doing
    predicated searches for all reachable nodes from a given node
    """
    def __init__(self):
        self._nodes = {}
        self._edges = {}

    @property
    def nodes(self) -> Set[DCGnode]:
        """list of nodes in DCG"""
        return self._nodes.values()

    def get_node(self, name: str) -> DCGnode:
        """return node by name"""
        return self._nodes[name]

    def create_node(self, name: str) -> DCGnode:
        """create node from name, and returns it"""
        if name in self._nodes:
            raise Exception(f"node {self._nodes[name]} exists")
        self._nodes[name] = DCGnode(name)
        return self._nodes[name]

    def add_node(self, node: DCGnode) -> None:
        """adds an already-existing node to the graph"""
        if node.name in self._nodes:
            raise Exception(f"node {node} exists as {self._nodes[node.name]}")
        self._nodes[node.name] = node

    @property
    def edges(self) -> Set[DCGedge]:
        """returns list of edges in DCG"""
        return self._edges.values()

    def get_edge(self, name: str) -> DCGedge:
        """return edge by name"""
        return self._edges[name]

    def create_edge(self, from_node: DCGnode, to_node: DCGnode) -> DCGedge:
        """create edge from a node to a node."""
        # pylint: disable=W0212
        edges_out = from_node.edges_out
        if len(list(filter(lambda e: e.to_node == to_node, edges_out))) > 0:
            raise Exception(f"edge from {from_node} to {to_node} exists")
        edge_name = f"edge_{len(self._edges.keys())}"
        edge = DCGedge(name=edge_name, from_node=from_node, to_node=to_node)
        self._edges[edge_name] = edge
        from_node.add_edge_out(edge)
        to_node.add_edge_in(edge)
        return self._edges[edge_name]
