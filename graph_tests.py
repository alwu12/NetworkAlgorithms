import unittest
import random
from unittest.mock import patch
import math
from graph import Graph
from erdos_renyi import generate_erdos_renyi_graph

class TestErdosRenyiGraph(unittest.TestCase):
    def test_num_vertices(self):
        """Test that the graph has the correct number of vertices."""
        n = 10
        graph = generate_erdos_renyi_graph(n)
        self.assertEqual(graph.get_num_nodes(), n)

    def test_num_edges_and_adjacency_list(self):
        """Test the number of edges and consistency with the adjacency list."""
        n = 5
        graph = generate_erdos_renyi_graph(n)
        edges = list(graph.get_edges())
        # Check number of edges matches get_num_edges()
        self.assertEqual(graph.get_num_edges(), len(edges))
        # Check adjacency list consistency
        for u, v in edges:
            # Ensure u and v are neighbors in the adjacency list
            self.assertIn(v, graph.get_neighbors(u), f"Vertex {v} not in {u}'s neighbors")
            self.assertIn(u, graph.get_neighbors(v), f"Vertex {u} not in {v}'s neighbors")
            # Ensure edges are valid: within range, no self-loops
            self.assertTrue(0 <= u < n, f"Vertex {u} out of range")
            self.assertTrue(0 <= v < n, f"Vertex {v} out of range")
            self.assertNotEqual(u, v, f"Self-loop detected: ({u}, {v})")

    def test_expected_number_of_edges(self):
        """Test that the number of edges is close to the expected value."""
        n = 100
        p = (2 * math.log(n)) / n
        expected_edges = p * (n * (n - 1)) / 2
        trials = 10
        total_edges = 0
        for _ in range(trials):
            graph = generate_erdos_renyi_graph(n)
            total_edges += graph.get_num_edges()
        avg_edges = total_edges / trials
        # Allow 20% deviation due to randomness
        self.assertAlmostEqual(avg_edges, expected_edges, delta=0.2 * expected_edges)

if __name__ == '__main__':
    unittest.main()