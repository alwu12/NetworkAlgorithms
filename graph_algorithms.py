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

