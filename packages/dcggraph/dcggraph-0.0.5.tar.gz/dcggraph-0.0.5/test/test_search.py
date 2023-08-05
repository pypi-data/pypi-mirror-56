#!/usr/bin/env python

import unittest
import re

from dcggraph import DCGnode, DCGedge, DCGgraph
from dcggraph.search import PredicateResult, DCGsearch

class TestDisjointNonCyclic(unittest.TestCase):

    def setUp(self):
        g = DCGgraph()
        self.g = g

        self.n0 = g.create_node("n0")
        self.n1 = g.create_node("n1")
        self.n2 = g.create_node("n2")
        self.n3 = g.create_node("n3")
        self.n4 = g.create_node("n4")
        g.create_edge(self.n0, self.n1)
        g.create_edge(self.n0, self.n2)
        g.create_edge(self.n1, self.n3)
        g.create_edge(self.n1, self.n4)

        self.m0 = g.create_node("m0")
        self.m1 = g.create_node("m1")
        self.m2 = g.create_node("m2")
        self.m3 = g.create_node("m3")
        self.m4 = g.create_node("m4")
        g.create_edge(self.m0, self.m1)
        g.create_edge(self.m0, self.m2)
        g.create_edge(self.m1, self.m3)
        g.create_edge(self.m1, self.m4)

    def test_no_predicate(self):
        s = DCGsearch(self.g)

        self.assertEqual(len(s.search(self.n0)), 5)
        self.assertEqual(len(s.search(self.n1)), 3)
        self.assertEqual(len(s.search(self.n2)), 1)
        self.assertEqual(len(s.search(self.n3)), 1)
        self.assertEqual(len(s.search(self.n4)), 1)

        self.assertEqual(len(s.search(self.m0)), 5)
        self.assertEqual(len(s.search(self.m1)), 3)
        self.assertEqual(len(s.search(self.m2)), 1)
        self.assertEqual(len(s.search(self.m3)), 1)
        self.assertEqual(len(s.search(self.m4)), 1)

    def test_even_predicate(self):
        """predicate always returns PASS/FAIL (never WAIT)"""
        really_run = True
        def even(node, visited, passed, failed):
            if not really_run:
                return PredicateResult.FAIL
            elif re.match("[a-z][02468]", node.name):
                return PredicateResult.PASS
            else:
                return PredicateResult.FAIL

        s1 = DCGsearch(self.g, even)

        self.assertEqual(len(s1.search(self.n0)), 3)
        self.assertEqual(len(s1.search(self.n1)), 1)
        self.assertEqual(len(s1.search(self.n2)), 1)
        self.assertEqual(len(s1.search(self.n3)), 0)
        self.assertEqual(len(s1.search(self.n4)), 1)

    def test_even_memo(self):
        """show that memo is caching results as expected for PASS/FAIL"""
        really_run = True
        def odd(node, visited, passed, failed):
            if not really_run:
                return PredicateResult.FAIL
            elif re.match("[a-z][13579]", node.name):
                return PredicateResult.PASS
            else:
                return PredicateResult.FAIL

        s1 = DCGsearch(self.g, odd)
        s2 = DCGsearch(self.g, odd)

        self.assertEqual(len(s1.search(self.n0)), 2)
        self.assertEqual(len(s1.search(self.n1)), 2)
        self.assertEqual(len(s1.search(self.n2)), 0)
        self.assertEqual(len(s1.search(self.n3)), 1)
        self.assertEqual(len(s1.search(self.n4)), 0)

        # now, show the memo cached results in the original 
        really_run = False
        self.assertEqual(len(s1.search(self.n0)), 2)
        self.assertEqual(len(s1.search(self.n1)), 2)
        self.assertEqual(len(s1.search(self.n2)), 0)
        self.assertEqual(len(s1.search(self.n3)), 1)
        self.assertEqual(len(s1.search(self.n4)), 0)

        self.assertEqual(len(s2.search(self.n0)), 0)
        self.assertEqual(len(s2.search(self.n1)), 0)
        self.assertEqual(len(s2.search(self.n2)), 0)
        self.assertEqual(len(s2.search(self.n3)), 0)
        self.assertEqual(len(s2.search(self.n4)), 0)

        really_run = True
        self.assertEqual(len(s1.search(self.n0)), 2)
        self.assertEqual(len(s1.search(self.n1)), 2)
        self.assertEqual(len(s1.search(self.n2)), 0)
        self.assertEqual(len(s1.search(self.n3)), 1)
        self.assertEqual(len(s1.search(self.n4)), 0)

        self.assertEqual(len(s2.search(self.n0)), 0)
        self.assertEqual(len(s2.search(self.n1)), 0)
        self.assertEqual(len(s2.search(self.n2)), 0)
        self.assertEqual(len(s2.search(self.n3)), 0)
        self.assertEqual(len(s2.search(self.n4)), 0)

class TestCyclic(unittest.TestCase):

    def setUp(self):
        g = DCGgraph()
        self.g = g

        self.n0 = g.create_node("n0")
        self.n1 = g.create_node("n1")
        self.n2 = g.create_node("n2")
        self.n3 = g.create_node("n3")
        self.n4 = g.create_node("n4")
        g.create_edge(self.n0, self.n1)
        g.create_edge(self.n0, self.n2)
        g.create_edge(self.n1, self.n3)
        g.create_edge(self.n1, self.n4)

        self.m0 = g.create_node("m0")
        self.m1 = g.create_node("m1")
        self.m2 = g.create_node("m2")
        self.m3 = g.create_node("m3")
        self.m4 = g.create_node("m4")
        g.create_edge(self.m0, self.m1)
        g.create_edge(self.m0, self.m2)
        g.create_edge(self.m1, self.m3)
        g.create_edge(self.m1, self.m4)

        self.p0 = g.create_node("p0")

        # connect two graphs
        g.create_edge(self.n0, self.m0)
        g.create_edge(self.m0, self.p0)
        g.create_edge(self.p0, self.n0)

    def test_no_predicate(self):
        s = DCGsearch(self.g)

        self.assertEqual(len(s.search(self.n0)), 11)
        self.assertEqual(len(s.search(self.n1)), 3)
        self.assertEqual(len(s.search(self.n2)), 1)
        self.assertEqual(len(s.search(self.n3)), 1)
        self.assertEqual(len(s.search(self.n4)), 1)

        self.assertEqual(len(s.search(self.m0)), 11)
        self.assertEqual(len(s.search(self.m1)), 3)
        self.assertEqual(len(s.search(self.m2)), 1)
        self.assertEqual(len(s.search(self.m3)), 1)
        self.assertEqual(len(s.search(self.m4)), 1)

        self.assertEqual(len(s.search(self.p0)), 11)

    def test_even_predicate(self):
        """predicate always returns PASS/FAIL (never WAIT)"""
        def even(node, visited, passed, failed):
            if re.match("[a-z][02468]", node.name):
                return PredicateResult.PASS
            else:
                return PredicateResult.FAIL

        s1 = DCGsearch(self.g, even)

        self.assertEqual(len(s1.search(self.n0)), 7)
        self.assertEqual(len(s1.search(self.n1)), 1)
        self.assertEqual(len(s1.search(self.n2)), 1)
        self.assertEqual(len(s1.search(self.n3)), 0)
        self.assertEqual(len(s1.search(self.n4)), 1)

        self.assertEqual(len(s1.search(self.m0)), 7)
        self.assertEqual(len(s1.search(self.m1)), 1)
        self.assertEqual(len(s1.search(self.m2)), 1)
        self.assertEqual(len(s1.search(self.m3)), 0)
        self.assertEqual(len(s1.search(self.m4)), 1)

        self.assertEqual(len(s1.search(self.p0)), 7)

    def test_wait_even_predicate(self):
        """even predicate returns WAIT UNTIL all subnodes resolved"""
        def even(node, visited, passed, failed):
            for edge in node.edges_out:
                if edge.to_node.name not in visited:
                    return PredicateResult.WAIT
            if re.match("[a-z][02468]", node.name):
                return PredicateResult.PASS
            else:
                return PredicateResult.FAIL

        s1 = DCGsearch(self.g, even)

        self.assertEqual(len(s1.search(self.n0)), 7)
        self.assertEqual(len(s1.search(self.n1)), 1)
        self.assertEqual(len(s1.search(self.n2)), 1)
        self.assertEqual(len(s1.search(self.n3)), 0)
        self.assertEqual(len(s1.search(self.n4)), 1)

        self.assertEqual(len(s1.search(self.m0)), 7)
        self.assertEqual(len(s1.search(self.m1)), 1)
        self.assertEqual(len(s1.search(self.m2)), 1)
        self.assertEqual(len(s1.search(self.m3)), 0)
        self.assertEqual(len(s1.search(self.m4)), 1)

        self.assertEqual(len(s1.search(self.p0)), 7)

    def test_unresolved_even_predicate(self):
        """
        even predicate returns WAIT if all subnodes PASS/FAIL. so
        n0, m0, p0 remain in WAIT until no more to visit, and end up in FAIL
        """ 
        def even(node, visited, passed, failed):
            for edge in node.edges_out:
                to_name = edge.to_node.name
                if (to_name not in passed) and (to_name not in failed):
                    return PredicateResult.WAIT
            if re.match("[a-z][02468]", node.name):
                return PredicateResult.PASS
            else:
                return PredicateResult.FAIL

        s1 = DCGsearch(self.g, even)

        self.assertEqual(len(s1.search(self.n0)), 4)
        self.assertEqual(len(s1.search(self.n1)), 1)
        self.assertEqual(len(s1.search(self.n2)), 1)
        self.assertEqual(len(s1.search(self.n3)), 0)
        self.assertEqual(len(s1.search(self.n4)), 1)

        self.assertEqual(len(s1.search(self.m0)), 4)
        self.assertEqual(len(s1.search(self.m1)), 1)
        self.assertEqual(len(s1.search(self.m2)), 1)
        self.assertEqual(len(s1.search(self.m3)), 0)
        self.assertEqual(len(s1.search(self.m4)), 1)

        self.assertEqual(len(s1.search(self.p0)), 4)

if __name__ == "__main__":
    unittest.main()

