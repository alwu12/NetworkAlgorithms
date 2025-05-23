# explanations for these functions are provided in requirements.py

from graph import Graph
from collections import deque, defaultdict

def get_diameter(graph: Graph) -> int:
	def bfs(g: Graph, source_node) -> int:
		longest_path = 0
		q = deque() #using a deque as a queue instead of a list because inserting
		#at the beginning of a list costs O(n)
		visited = set()
		q.append(source_node)
		visited.add(source_node)
		distance = defaultdict(int)
		

		while(len(q) > 0):

			node = q.popleft()
			for neighbor in g.get_neighbors(node):
				if neighbor not in visited:
					q.append(neighbor)
					visited.add(neighbor)
					distance[neighbor] = distance[node]+1
					longest_path = max(longest_path,distance[neighbor])
		return longest_path
	

	max_length = 0
	for i in range(0,graph.get_num_nodes()):
		max_length = max(max_length,bfs(graph,i))
	
	return max_length
	





def get_clustering_coefficient(graph: Graph) -> float:
	raise NotImplementedError


def get_degree_distribution(graph: Graph) -> dict[int, int]:
	raise NotImplementedError
