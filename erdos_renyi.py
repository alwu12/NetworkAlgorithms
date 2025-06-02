import random
import math
from graph import Graph
from typing import List, Tuple

def generate_erdos_renyi_graph(n: int) -> Graph:
    p = (2 * math.log(n)) / n
    edges: List[Tuple[int, int]] = []
    
    v = 1
    w = -1
    while v < n:
        r = random.random()  # Uniform in [0, 1)
        w = w + 1 + math.floor(math.log(1 - r) / math.log(1 - p))
        while w >= v and v < n:
            w = w - v
            v = v + 1
        if v < n:
            edges.append((v, w))
    
    return Graph(n, edges)
