from benchmark_get_averages import *

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    x_fit = x[2:-1]#this ignores the first 5 values when making our line of best fit
    y_fit = y[2:-1]
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
    #plt.title(f"{algorithm_name.replace('_', ' ').title()} Performance")
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

    for filename in files:
        filepath = base_directory / filename
        data = load_degree_distribution(filepath)
        x_vals = sorted(data.keys())
        y_vals = [data[x] for x in x_vals]

        # Lin-Lin plot in blue, points only
        plt.figure(figsize=(6, 4))
        plt.plot(x_vals, y_vals, marker='o', linestyle='None', color='blue')
        plt.xlabel('Degree')
        plt.ylabel('Count')
        plt.title(f'Degree Distribution (Lin-Lin) - {filename}')
        plt.grid(True)
        plt.show()

        # Log-Log plot in green, points only, base 2 scale, numeric ticks
        plt.figure(figsize=(6, 4))
        plt.loglog(x_vals, y_vals, marker='o', linestyle='None', color='green')
        plt.xlabel('Degree (log scale)')
        plt.ylabel('Count (log scale)')
        plt.title(f'Degree Distribution (Log-Log) - {filename}')
        plt.grid(True, which='both')

        ax = plt.gca()
        ax.set_xscale('log', base=2)
        ax.set_yscale('log')

        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        ax.xaxis.get_major_formatter().set_scientific(False)
        ax.xaxis.get_major_formatter().set_useMathText(False)

        ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
        ax.yaxis.get_major_formatter().set_scientific(False)
        ax.yaxis.get_major_formatter().set_useMathText(False)

        plt.show()

if __name__ == '__main__':
    #data = return_all_data()
    #for i in GRAPH_ALGORITHMS:
    #    plot_algorithm(data, i)

    plot_degree_distributions()