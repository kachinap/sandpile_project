import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Parameters
N = 50           # gridsize
K = 3            # slope at critical point
V = 7            # initial slope of interior cells 
num_avalanches = 1000  # number of avalanches to simulate

# for reproducibility of random grain placement:
np.random.seed(42)

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

def add_grain_run_avalanche(grid):
    i = np.random.randint(1, N-1)
    j = np.random.randint(1, N-1)
    grid[i, j] += 1
    return run_avalanche(grid)

def simulate_avalanches(num_avalanches):
    # Initialize and reach critical state
    grid = initialize_grid()
    grid = run_to_equilibrium(grid)
    
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
    plt.title(f'Avalanche Size Distribution (N={N}, K={K}, {len(avalanche_sizes)} avalanches)')
    plt.grid(which="both", ls="-")
    plt.show()

# Main execution
if __name__ == "__main__":
    print(f"Simulating {num_avalanches} avalanches...")
    avalanche_sizes = simulate_avalanches(num_avalanches)
    
    print("Avalanche size statistics:")
    print(f"Total avalanches: {len(avalanche_sizes)}")
    print(f"Minimum size: {min(avalanche_sizes)}")
    print(f"Maximum size: {max(avalanche_sizes)}")
    print(f"Average size: {np.mean(avalanche_sizes):.2f}")
    
    # Plot the distribution
    plot_avalanche_distribution(avalanche_sizes)