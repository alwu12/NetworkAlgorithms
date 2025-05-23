# explanations for member functions are provided in requirements.py
# each file that uses a graph should import it from this file.

from collections.abc import Iterable

class Graph:
	def __init__(self, num_nodes: int, edges: Iterable[tuple[int, int]]):
		self.num_nodes = num_nodes
		self.edges = edges

		self.adjacency_list = [[] for _ in range(num_nodes)]
		#one list for each node

		for i in self.edges:
			self.adjacency_list[i[0]].append(i[1])
			self.adjacency_list[i[1]].append(i[0])



	def get_num_nodes(self) -> int:
		return self.num_nodes

	def get_num_edges(self) -> int:
		return len(self.edges)

	def get_neighbors(self, node: int) -> Iterable[int]:
		return self.adjacency_list[node]

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
