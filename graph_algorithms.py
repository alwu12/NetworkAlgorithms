# explanations for these functions are provided in requirements.py

from graph import Graph
from collections import deque, defaultdict
from random import randint, seed



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


def get_d_ordering(graph: Graph) -> tuple[list[int], list[list[int]]]:
	n = graph.get_num_nodes()
	L = []
	dv = [len(graph.get_neighbors(v)) for v in range(n)]#gets the degree of each vertex
	max_degree = max(dv)
	D = [[] for _ in range(max_degree+1)] #list of lists that determine which nodes are of which degree
	#for example: D = [[], [1, 2, 3], [4]] means 0 nodes of 0 degree, 3 of 1 degree and 1 of 2 degree
	
	for i in range(n):
		D[dv[i]].append(i) #append current vertex to their degree list
		#for example 1 would get put in the 2nd list because that would be it's degree in dv
	
	N_v = [[] for _ in range(n)] #this will track neighbors of v that come before it in the ordering.
		
	HL = {i:False for i in range(n)} #hash table to check whether a vertex is in L
	k = 0 #used to track degeneracy
	for _ in range(n):
		#Let i be the smallest index such that D[i] is nonempty.

		for i in range(len(D)):
			if D[i]:#if the bucket is empty, find a bucket that isnt empty
				v = D[i].pop() 
				'''
				Select a vertex v from D[i]. Add v to the beginning of L and remove it
				from D[i]. Mark v as being in L (e.g., using a hash table, HL).
				'''
				k = max(k,i)
				L.append(v)
				HL[v] = True
				for w in graph.get_neighbors(v):
					if not HL[w]:
						dv[w] -= 1
						D[dv[w]+1].remove(w)
						D[dv[w]].append(w)
						N_v[v].append(w)
				break

	return L[::-1], N_v


def get_triangles(graph: Graph) -> int:
	triangle_count = 0
	L, nv = get_d_ordering(graph)
	for v in L:
		neighbors_before_v = nv[v]

		for i in range(len(neighbors_before_v)):
			u = neighbors_before_v[i]
			for j in range(len(neighbors_before_v)):
				w = neighbors_before_v[j]
				if w < u:
					continue
				if graph.is_adjacent(u,w):
					triangle_count+=1
	return triangle_count
		
'''
def get_triangles(graph: Graph) -> int:
    triangle_count = 0
    num_nodes = graph.get_num_nodes()
    
    for u in range(num_nodes):
        neighbors_u = graph.get_neighbors(u)
        #neighbors_u = sorted(neighbors_u)  # sort to enforce ordering
        
        for v in neighbors_u:
            if v < u:
                continue  # skip to avoid double counting
            
            for w in neighbors_u:
                # enforce w > v to avoid repeats
                if w <= v:
                    continue
                
                if graph.is_adjacent(v, w):
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

