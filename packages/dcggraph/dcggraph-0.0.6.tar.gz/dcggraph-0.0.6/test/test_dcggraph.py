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
        n2 = DCGnode("foo3")
        n3 = DCGnode("foo")
        g.add_node(n2)
        self.assertEqual(n0, g.get_node(n0.name))
        self.assertNotEqual(n0, g.get_node(n1.name))
        self.assertNotEqual(n0, g.get_node(n2.name))
        self.assertNotEqual(n0, n1)
        self.assertNotEqual(n0, n2)
        self.assertEqual(len(n0.edges_out), 0)
        self.assertEqual(len(n0.edges_in), 0)
        with self.assertRaisesRegex(Exception, "node .* exists"):
            g.create_node("foo")
        with self.assertRaisesRegex(Exception, "node .* exists"):
            g.create_node("foo3")
        with self.assertRaisesRegex(Exception, "node .* exists as "):
            g.add_node(n3)
        self.assertEqual(len(g.nodes), 3)

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

        g.create_edge(n0, n1, True)
        self.assertEqual(len(g.edges), 3)

        # adding edges to nodes checks
        self.assertEqual(len(n0.edges_out), 2)
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

    def test_deep_equal(self):
        """make sure that edge order doesn't matter"""
        g0 = DCGgraph()
        g1 = DCGgraph()

        g0n0 = g0.create_node("n0")
        g0n1 = g0.create_node("n1")
        g0n2 = g0.create_node("n2")
        g0n3 = g0.create_node("n3")
        g0.create_edge(g0n0, g0n1)
        g0.create_edge(g0n0, g0n2)
        g0.create_edge(g0n2, g0n3)

        g1n3 = g1.create_node("n3")
        g1n2 = g1.create_node("n2")
        g1n1 = g1.create_node("n1")
        g1n0 = g1.create_node("n0")
        g1.create_edge(g1n0, g1n1)
        g1.create_edge(g1n0, g1n2)
        g1.create_edge(g1n2, g1n3)
        g1.create_edge(g1n1, g1n3)

        self.assertEqual(g0n0.deep_equal(g1n0), False)
        self.assertEqual(g0n1.deep_equal(g1n1), False)
        self.assertEqual(g0n2.deep_equal(g1n2), True)
        self.assertEqual(g0n3.deep_equal(g1n3), True)

if __name__ == "__main__":
    unittest.main()

