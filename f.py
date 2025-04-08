import numpy as np
import time
import matplotlib.pyplot as plt

start_time = time.time()

# Parameters
N = 200           # gridsize
K = 3            # slope at critical point
V = 7            # initial slope of interior cells 
num_avalanches = 20000  # number of avalanches to simulate

# for reproducibility of random grain placement:
np.random.seed(43)

def initialize_grid():
    grid = np.zeros((N, N), dtype=int)
    grid[1:-1, 1:-1] = V
    return grid

def topple(grid):
    grid = grid.copy()
    gridchanges = np.zeros((N, N), dtype=int)
    topple_count = 0
    # process only interior cells; boundaries remain fixed
    for i in range(1, N-1):
        for j in range(1, N-1):
            if grid[i, j] > K:
                gridchanges[i, j] -= 4
                gridchanges[i+1, j] += 1
                gridchanges[i-1, j] += 1
                gridchanges[i, j+1] += 1
                gridchanges[i, j-1] += 1
                topple_count += 1
    grid += gridchanges
    grid[0, :] = 0  
    grid[-1, :] = 0
    grid[:, 0] = 0 
    grid[:, -1] = 0
    return topple_count, grid

def run_to_equilibrium(grid):
    grid = grid.copy()
    while True:
        count, grid = topple(grid)
        if count == 0:
            break
    return grid

def run_avalanche(grid):
    avalanche_size = 0
    while True:
        count, grid = topple(grid)
        if count == 0:
            break
        avalanche_size += count
    return avalanche_size, grid

def Random():
    return np.random.randint(1,N-1, size=2)

def Edges():
    borders = {
        'top': (1, 11, 1, N),        # Row between 0-9, Column between 0-199
        'bottom': (190, N, 1, N),  # Row between 190-199, Column between 0-199
        'left': (1, N, 1, 11),       # Row between 0-199, Column between 0-9
        'right': (1, N, 190, N)    # Row between 0-199, Column between 190-199
    }
    # Randomly choose a border and unpack the ranges
    border = np.random.choice(list(borders.keys()))
    i_range, j_range = borders[border][:2], borders[border][2:]
    # Randomly select an index from the chosen border
    i = np.random.randint(i_range[0], i_range[1])
    j = np.random.randint(j_range[0], j_range[1])
    return i, j

def add_grain_run_avalanche(grid):
    #Choose a random place in a 10x10 grid in the middle of the sandpile
    if function == 1:
        i,j = Random()
    if function == 2:
        i,j = [100,100]
    if function == 3:
        i,j = Edges()
    grid[i, j] += 1
    return run_avalanche(grid)

def simulate_avalanches(num_avalanches):
    # Load the stable state from Z = 7:
    grid = np.load('stable_starting_state.npy')
    
    # Simulate avalanches
    avalanche_sizes = []
    for _ in range(num_avalanches):
        size, grid = add_grain_run_avalanche(grid)
        avalanche_sizes.append(size)  
    return avalanche_sizes

def plot_avalanche_distribution(avalanche_sizes):
    # Count frequency of each avalanche size
    size_counts = {} # empty dictionary: size -> count
    for size in avalanche_sizes:
        if size in size_counts: # check if we've seen this size before
            size_counts[size] += 1
        else:
            size_counts[size] = 1 # first time we've seen this size
    
    # Prepare data for plotting
    sizes = np.array(sorted(size_counts.keys())) # x-asix: sorted sizes (keys in dictionary)
    counts = np.array([size_counts[size] for size in sizes]) # y-axis: counts for each size

    # Create log-log plot
    plt.figure(figsize=(10, 6))
    plt.loglog(sizes, counts, 'bo', markersize=5)
    plt.xlabel('Avalanche Size')
    plt.ylabel('Frequency')
    plt.title(f'Avalanche Size Distribution (N={N}, K={K}, {len(avalanche_sizes)} avalanches) ({name})')
    plt.grid(which="both", ls="-")
    
    plt.figure(figsize=(10,6))
    bins = np.logspace(0, np.log10(max(avalanche_sizes[0:])+1), 50)
    plt.hist(avalanche_sizes[0:], bins=bins, edgecolor='k', color='teal')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Avalanche size (number of topplings)')
    plt.ylabel('Number of avalanches')
    plt.title(f'Avalanche Size Histogram (N={N}, K={K}, {len(avalanche_sizes)} avalanches) ({name})')
    plt.show()

#Three ways to generate grains: [Randomly, Middle only, Near borders]
methods = [1,3]

# Main execution
if __name__ == "__main__":
    for function,name in zip(methods,['Random','Edges']):
        print(f"Simulating {num_avalanches} grains added at {name}...")
        avalanche_sizes = simulate_avalanches(num_avalanches)
        
        print("Avalanche size statistics:")
        print(f"Total avalanches: {len(avalanche_sizes)}")
        print(f"Minimum size: {min(avalanche_sizes)}")
        print(f"Maximum size: {max(avalanche_sizes)}")
        print(f"Average size: {np.mean(avalanche_sizes):.2f} \n")
        
        # Plot the distribution
        plot_avalanche_distribution(avalanche_sizes)
    end_time = time.time()
    run_time = (end_time - start_time)/60
    print(f'Script ran for {run_time:.2f} min') 