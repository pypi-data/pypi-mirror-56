"""
This file contains the base classes for the dcggraph package.
"""

from typing import List, Text

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

    @property
    def name(self)->str:
        """returns the node name"""
        return self._name

    @property
    def edges_in(self)->List["DCGedge"]:
        """returns the list of edges pointing in to this node"""
        return self._edges_in.values()

    @property
    def edges_out(self)->List["DCGedge"]:
        """returns the list of edges pointing out of this node"""
        return self._edges_out.values()

    def add_edge_in(self, edge: "DCGedge") -> None:
        """adds an inward-pointing edge"""
        if (edge.name in self._edges_out) or (edge.name in self._edges_in):
            raise Exception(f"{edge} is already connected within {self}")
        if edge.to_node != self:
            raise Exception(f"{edge} is not connected to {self}")
        self._edges_in[edge.name] = edge

    def add_edge_out(self, edge: "DCGedge") -> None:
        """adds an outward-pointing edge"""
        if (edge.name in self._edges_out) or (edge.name in self._edges_in):
            raise Exception(f"{edge} is already connected to {self}")
        if edge.from_node != self:
            raise Exception(f"{edge} is not connected from {self}")
        self._edges_out[edge.name] = edge

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
    def nodes(self)->List[DCGnode]:
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

    @property
    def edges(self)->List[DCGedge]:
        """returns list of edges in DCG"""
        return self._edges.values()

    def get_edge(self, name: str) -> DCGedge:
        """return edge by name"""
        return self._edges[name]

    def create_edge(self, from_node: DCGnode, to_node: DCGnode) -> DCGedge:
        """create edge from a node to a node"""
        # pylint: disable=W0212
        edges_out = from_node.edges_out
        if len(list(filter(lambda x: x.to_node == to_node, edges_out))) > 0:
            raise Exception(f"edge from {from_node} to {to_node} exists")
        edge_name = f"edge_{len(self._edges.keys())}"
        edge = DCGedge(name=edge_name, from_node=from_node, to_node=to_node)
        self._edges[edge_name] = edge
        from_node.add_edge_out(edge)
        to_node.add_edge_in(edge)
        return self._edges[edge_name]
