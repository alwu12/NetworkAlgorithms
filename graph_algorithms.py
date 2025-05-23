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






def get_clustering_coefficient(graph: Graph) -> float:
	def get_max_edges(num_neighbors: int):
		#gets the max amount of edges that a nodes neighbors can have
		#If a node A has 3 neighbors: B, C, and D, the possible edges between neighbors are:
		#B-C, B-D, C-D → 3 possible edges
		return num_neighbors*(num_neighbors-1)//2
	
	clustering_coefficients = {}
	
	for u in range(0,graph.get_num_nodes()): #calculate the clustering coefficient for i
		neighbors = graph.get_neighbors(u)
		max_edges = get_max_edges(len(neighbors))
		actual_edges = 0
		for v in neighbors: #for each neighbor's neighbor 
			#for example for a, we have 3 neighbors b,c,d
			#this for loop is meant to check each b c and d to see if there is an edge between them
			if v < u: #dont remember exactly but we discussed a heuristic in class where U<V<W
				#this is so we dont count edges multiple times
				continue
			v_neighbors = graph.get_neighbors(v)
			for w in v_neighbors:
				if w > v and graph.is_adjacent(u,w):
					actual_edges+=1
		#print(f"actual edges for {u}: {actual_edges}")
		#print(f"max edges for {u}: {max_edges}")
		clustering_coefficients[u] = actual_edges/max_edges #add to our dict to compute average later

	
	#compute average
	#print(f'clustering_coefficients: {clustering_coefficients}')
	#return sum(clustering_coefficients.values())/(len(clustering_coefficients))
	non_zero_coeffs = [coeff for coeff in clustering_coefficients.values() if coeff > 0]
	if not non_zero_coeffs:  # Avoid division by zero
		return 0
	return sum(non_zero_coeffs) / len(non_zero_coeffs)
	



def get_degree_distribution(graph: Graph) -> dict[int, int]:
	degree_distribution = defaultdict(int)
	for i in range(0,graph.get_num_nodes()): #get the degrees of each node
		degree_distribution[len(graph.adjacency_list[i])] += 1
	#a dict of the format{degree:num nodes with that degree}
	return degree_distribution

