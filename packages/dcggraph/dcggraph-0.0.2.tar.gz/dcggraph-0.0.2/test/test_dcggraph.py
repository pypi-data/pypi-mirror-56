#!/usr/bin/env python

import unittest

from dcggraph import DCGnode, DCGedge, DCGgraph

class TestDCGgraph(unittest.TestCase):

    def test_basic_graph(self):
        # graph init checks
        g = DCGgraph()
        self.assertEqual(len(g.nodes), 0)
        self.assertEqual(len(g.edges), 0)
        with self.assertRaises(Exception):
            g.get_node("foo")
        with self.assertRaises(Exception):
            g.get_edge("edge_0")

        # creating nodes checks
        n0 = g.create_node("foo")
        n1 = g.create_node("foo2")
        self.assertEqual(n0, g.get_node(n0.name))
        self.assertNotEqual(n0, g.get_node(n1.name))
        self.assertNotEqual(n0, n1)
        self.assertEqual(len(n0.edges_out), 0)
        self.assertEqual(len(n0.edges_in), 0)
        with self.assertRaisesRegex(Exception, "node .* exists"):
            g.create_node("foo")
        self.assertEqual(len(g.nodes), 2)

        # creating edges checks
        e0 = g.create_edge(n0, n1)
        e1 = g.create_edge(n1, n0)
        self.assertEqual(e0, g.get_edge(e0.name))
        self.assertNotEqual(e0, g.get_edge(e1.name))
        self.assertNotEqual(e0, e1)
        self.assertEqual(e0.from_node, n0)
        self.assertEqual(e0.to_node, n1)
        with self.assertRaisesRegex(Exception, "edge from .* exists"):
            g.create_edge(n0, n1)
        self.assertEqual(len(g.edges), 2)

        # adding edges to nodes checks
        self.assertEqual(len(n0.edges_out), 1)
        self.assertEqual(len(n0.edges_in), 1)
        n2 = g.create_node("bar")
        n3 = g.create_node("bar2")
        e2 = g.create_edge(n2, n3)
        with self.assertRaisesRegex(Exception, ".* is already connected"):
            n0.add_edge_in(e1)
        with self.assertRaisesRegex(Exception, ".* is already connected"):
            n0.add_edge_out(e0)
        with self.assertRaisesRegex(Exception, ".* is not connected to"):
            n0.add_edge_in(e2)
        with self.assertRaisesRegex(Exception, ".* is not connected from"):
            n0.add_edge_out(e2)

if __name__ == "__main__":
    unittest.main()

