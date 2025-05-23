# explanations for these functions are provided in requirements.py

from graph import Graph
from collections import deque, defaultdict
from random import randint, seed



'''
def get_diameter_naive(graph: Graph) -> int: #gets exact diameter but slow
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
					distance[neighbor] = distance[node]+1 #count longest path by taking the path from the previous node
					#and adding +1 to it
					longest_path = max(longest_path,distance[neighbor])
		return longest_path
	

	max_length = 0
	for i in range(0,graph.get_num_nodes()):
		max_length = max(max_length,bfs(graph,i))
	
	return max_length
'''

def get_diameter(graph: Graph) -> int: #use a heuristic instead of getting exact diameter from bfsing all nodes
	def bfs(g: Graph, source_node) -> int:
		longest_path = 0
		furthest_node = source_node #should be equivalent to 0
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
					distance[neighbor] = distance[node]+1 #count longest path by taking the path from the previous node
					#and adding +1 to it
					if distance[neighbor] > longest_path:
						longest_path = distance[neighbor]
						furthest_node = neighbor
		return longest_path, furthest_node
	

	# Step 1: Let r be a random vertex and set Dmax = 0
	r = randint(0,graph.get_num_nodes()-1)
	dmax = 0

	
	# Step 2: Perform a BFS from r
	furthest_path,w = bfs(graph,r)
	# Step 3: Select the farthest node, w, in this BFS
	#         If the distance from r to w is larger than Dmax:
	#         - update Dmax to this distance
	#         - set r = w
	#         - repeat the BFS from the new r
	dmax = furthest_path
	r = w
	w_furthest_path,w = bfs(graph,r)

	dmax = max(w_furthest_path,dmax)

	return dmax

'''
def degeneracy_ordering_with_Nv(graph): # for get_clustering_coefficient
	num_nodes = graph.get_num_nodes()
	degree = [len(graph.get_neighbors(v)) for v in range(num_nodes)]
	D = defaultdict(deque)
	for v in range(num_nodes):
		D[degree[v]].append(v)

	position = list(degree)  # current dv values
	in_L = [False] * num_nodes
	Nv = [[] for _ in range(num_nodes)]
	L = []
	k = 0

	for _ in range(num_nodes):
		i = 0
		while i not in D or not D[i]:
			i += 1
		k = max(k, i)
		v = D[i].popleft()
		in_L[v] = True
		L.insert(0, v)  # add to beginning of L

		for w in graph.get_neighbors(v):
			if not in_L[w]:
				Nv[w].append(v)

				old_d = position[w]
				position[w] -= 1
				new_d = position[w]

				D[old_d].remove(w)
				D[new_d].append(w)

	return k, L, Nv


def get_triangles(graph: Graph) -> float: #for get_clustering_coefficient
	_, ordering, Nv = degeneracy_ordering_with_Nv(graph)

	triangle_count = 0
	for v in ordering:
		neighbors = Nv[v]
		for i in range(len(neighbors)):
			u = neighbors[i]
			for j in range(i + 1, len(neighbors)):
				w = neighbors[j]
				if graph.is_adjacent(u, w):
					triangle_count += 1
	return triangle_count
'''



def get_clustering_coefficient(graph: Graph) -> float:
	total_triplets = 0
	triangle_count = get_triangles(graph)
	for v in range(graph.get_num_nodes()):
		deg = len(graph.get_neighbors(v))
		total_triplets += deg * (deg - 1) // 2

	if total_triplets == 0:
		return 0.0

	return (3 * triangle_count) / total_triplets
	



def get_degree_distribution(graph: Graph) -> dict[int, int]:
	degree_distribution = defaultdict(int)
	for i in range(0,graph.get_num_nodes()): #get the degrees of each node
		degree_distribution[len(graph.adjacency_list[i])] += 1
	#a dict of the format{degree:num nodes with that degree}
	return degree_distribution

