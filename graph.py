# explanations for member functions are provided in requirements.py
# each file that uses a graph should import it from this file.

from collections.abc import Iterable

class Graph:
	def __init__(self, num_nodes: int, edges: Iterable[tuple[int, int]]):
		self.num_nodes = num_nodes
		self.edges = edges

		self.adjacency_list = [set() for _ in range(num_nodes)]
		#one list for each node

		for u,v in self.edges:
			self.adjacency_list[u].add(v)
			self.adjacency_list[v].add(u)


	def get_num_nodes(self) -> int:
		return self.num_nodes

	def get_num_edges(self) -> int:
		return len(self.edges)
	
	def get_edges(self) -> Iterable[tuple[int, int]]:
		return self.edges

	def get_neighbors(self, node: int) -> Iterable[int]:
		return self.adjacency_list[node]
	
	def is_adjacent(self, node1: int, node2: int):
		if node2 in self.adjacency_list[node1]:
			return True
		return False

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
