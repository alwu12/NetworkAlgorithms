from benchmark_get_averages import *

import matplotlib.pyplot as plt
import numpy as np



GRAPH_ALGORITHMS = [
    'diameter',
    'clustering_coefficient'
]



def plot_alg(data, label, markersize, color, legend_handles):
    #data is dataset of size+time running
    #label is which permutation
    #markersize is how big we want our dots to be
    #color is color of the dot and line
    #basex and basey refer to the base of the logarithm used
    x_vals = []
    y_vals = []
    print(f'data: {data}')
    for x, y in sorted(data.items()):
        x_vals.append(x)
        y_vals.append(y)

    

    
    # Plot all points at once to avoid duplicate legends
    plt.plot(x_vals, y_vals, '.', label=label, markersize=markersize, color=color)
    #plt.loglog(x_vals, y_vals, '-', color=color)  # Line connecting the dots
    

    x = np.array(x_vals)
    y = np.array(y_vals)
    x_fit = x[2:]#this ignores the first 5 values when making our line of best fit
    y_fit = y[2:]
    logx = np.log2(x_fit)
    logy = np.log2(y_fit)
    m, b = np.polyfit(logx, logy, 1)


    equation = f"y = {m:.5f} * log N + {b:.2f}"
    

    plt.plot(x_fit, 2 ** (m * logx + b), color=color)
    legend_handles[label] = plt.Line2D([0], [0], marker='o', color='red', label=f"{label} ({equation})", markersize=6, linestyle='None')
    
def plot_algorithm(data, algorithm_name):
    # Plot for different permutations
    legend_handles = {}
    plot_alg(data[algorithm_name], algorithm_name, 6, 'red',legend_handles)
    

    # Set the plot scale and labels
    plt.xscale('log', base=2)
    plt.yscale('linear')
    plt.xlabel("Input Size")
    plt.ylabel(algorithm_name)
    plt.yticks()
    plt.title(f"{algorithm_name.replace('_', ' ').title()} Performance")
    #plt.legend(handles=[legend_handles['ALMOST_SORTED'], legend_handles['ALTERNATING'], legend_handles['UNIFORMLY_DISTRIBUTED']])
    plt.legend(handles=list(legend_handles.values()))
    plt.grid(True)
    plt.show()


def plot_degree_distribution(data):
    legend_handles = {}
    plot_alg(data['degree_distribution'], 'degree_distribution', 6, 'red',legend_handles)
    

    # Set the plot scale and labels
    plt.xscale('log', base=2)
    plt.yscale('linear')
    plt.xlabel("Input Size")
    plt.ylabel("Waste")
    plt.yticks()
    plt.title(f"{algorithm_name.replace('_', ' ').title()} Performance")
    #plt.legend(handles=[legend_handles['ALMOST_SORTED'], legend_handles['ALTERNATING'], legend_handles['UNIFORMLY_DISTRIBUTED']])
    plt.legend(handles=list(legend_handles.values()))
    plt.grid(True)
    plt.show()

def load_degree_distribution(file_path: Path):
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                degree, count = line.split(',')
                data[int(degree)] = int(count)
    return data

def plot_degree_distributions(base_directory: Path = Path("data/degree_distribution")):
    files = ['degree_distribution_1000.csv', 'degree_distribution_10000.csv', 'degree_distribution_100000.csv']
    colors = ['blue', 'green', 'orange']
    
    plt.figure(figsize=(12, 5))
    
    # Lin-Lin plot
    plt.subplot(1, 2, 1)
    for filename, color in zip(files, colors):
        filepath = base_directory / filename
        data = load_degree_distribution(filepath)
        x_vals = sorted(data.keys())
        y_vals = [data[x] for x in x_vals]
        plt.plot(x_vals, y_vals, marker='o', linestyle='-', color=color, label=filename)
    plt.xlabel('Degree')
    plt.ylabel('Count')
    plt.title('Degree Distribution (Lin-Lin scale)')
    plt.legend()
    plt.grid(True)

    # Log-Log plot
    plt.subplot(1, 2, 2)
    for filename, color in zip(files, colors):
        filepath = base_directory / filename
        data = load_degree_distribution(filepath)
        x_vals = np.array(sorted(data.keys()))
        y_vals = np.array([data[x] for x in x_vals])
        plt.loglog(x_vals, y_vals, marker='o', linestyle='-', color=color, label=filename)
    plt.xlabel('Degree (log scale)')
    plt.ylabel('Count (log scale)')
    plt.title('Degree Distribution (Log-Log scale)')
    plt.legend()
    plt.grid(True, which='both')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    data = return_all_data()
    for i in GRAPH_ALGORITHMS:
        plot_algorithm(data, i)

    plot_degree_distributions()