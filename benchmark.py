import csv
from enum import Enum, unique
import random, time

from pathlib import Path

import requirements
from erdos_renyi import generate_erdos_renyi_graph
from graph import Graph

DATA_DIRECTORY = Path('data')
DATA_DIRECTORY.mkdir(exist_ok=True) #if directory already exists, the parameter prevents an error from being raised

@unique
class PermutationType(Enum):
    ERDOS_RENYI = 'erdos_renyi'

GRAPH_ALGORITHMS = {
    #'diameter' : requirements.get_diameter,
    'clustering_coefficient' : requirements.get_clustering_coefficient
    #'degree_distribution' : requirements.get_degree_distribution
}

def get_data_path(algorithm_name: str, permutation: PermutationType) -> Path:
    directory = DATA_DIRECTORY/algorithm_name #creates a subdirectory for that sorting algorithm.
    directory.mkdir(parents=True, exist_ok=True) #ensures the subdirectory exists.

    return (directory / permutation.name).with_suffix(suffix='.csv')# creates a file path like:
#data/shell_sort3/RANDOM.csv


def save_data(algorithm_name: str, size: int, permutation:PermutationType, result) -> None:
    file_path = get_data_path(algorithm_name,permutation)

    with open(file_path,mode='a', newline='') as file:#appends to end of a file
        writer = csv.writer(file)
        writer.writerow([size,result])

'''
def generate_random_list(size: int, permutation: PermutationType) -> list[float]:
    nums = [round(random.uniform(0.0, 0.35), 4) for _ in range(size)]

    match permutation:
        case PermutationType.RANDOMLY_DISTRIBUTED:
            random.shuffle(nums)

    return nums
'''



def run_benchmark(size: int)->None:
    for permutation in PermutationType:
        graph = generate_erdos_renyi_graph(size)
        #these are used to satisfy the positional arguments in each algorithm because they need both assignment and free_space
        

        for algorithm_name, algorithm in GRAPH_ALGORITHMS.items():
            #copy the list to ensure each algorithm works with the same input
            #start_time_ns = time.process_time_ns()

            result = algorithm(graph)
            #get_diameter(graph: Graph) -> int
            #get_clustering_coefficient(graph: Graph) -> float:
            #get_degree_distribution(graph: Graph) -> dict[int, int]:

            #end_time_ns = time.process_time_ns()
            #elapsed_time_ns = end_time_ns - start_time_ns

            save_data(algorithm_name,size,permutation,result)

def run_benchmarks():  # should do 10 runs of up to 2^20 with half increments
    for round_num in range(80):  # 10 runs total
        print(f"\n=== Round {round_num + 1}/10 ===")

        exp = 1
        while exp <= 18:
            size = int(2 ** exp)
            print(f"Running benchmark for size: {size} or (2^{exp})")
            start_time_ns = time.process_time_ns()

            run_benchmark(size)

            end_time_ns = time.process_time_ns()
            elapsed_time_ns = end_time_ns - start_time_ns
            print(f"Benchmark completed in {elapsed_time_ns / 1_000_000:.2f} ms")

            exp += 0.5

def save_degree_distribution(degree_counts: dict[int, int], n: int) -> None:
    directory = Path("data") / "degree_distribution"
    directory.mkdir(parents=True, exist_ok=True)  # make sure folder exists

    filename = f"degree_distribution_{n}.csv"
    filepath = directory / filename
    
    with open(filepath, mode='w', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(['degree', 'count'])  # optional header
        for degree, count in sorted(degree_counts.items()):
            writer.writerow([degree, count])
    
    print(f"Saved degree distribution for n={n} to {filepath}")


def save_all_degree_distributions():
    for n in [1000, 10_000, 100_000]:
        print(f"Generating graph with {n} vertices...")
        graph = generate_erdos_renyi_graph(n)
        degree_counts = requirements.get_degree_distribution(graph)
        save_degree_distribution(degree_counts, n)

if __name__ == "__main__":
    save_all_degree_distributions()
    #run_benchmarks()
    #run_benchmarks_alternating()