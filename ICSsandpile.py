import numpy as np
import matplotlib.pyplot as plt

N = 200          # gridsize
K = 3            # slope at critical point
num_iterations = 100000  # number of grains to add

def initialize_grid():
    # stable grid (all cells at 0)
    grid = np.zeros((N, N), dtype=int)
    return grid

def topple(grid):
    # performs one synchronous update of the grid
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
    return topple_count # number of topplings that occurred

def run_avalanche(grid):
    # runs the avalanche until no cell is unstable
    avalanche_size = 0
    while True:
        count = topple(grid)
        if count == 0:
            break
        avalanche_size += count
    return avalanche_size # total number of topplings during the avalanche

grid = initialize_grid()
avalanche_sizes = []  # to record the number of topplings per avalanche

# main loop: add one grain and let the system relax
for it in range(num_iterations):
    # add a grain to a random interior cell
    i = np.random.randint(1, N-1)
    j = np.random.randint(1, N-1)
    grid[i, j] += 1

    avalanche = run_avalanche(grid)
    avalanche_sizes.append(avalanche)

print("Simulation complete")
print("Average avalanche size:", np.mean(avalanche_sizes))
print("Max avalanche size:", np.max(avalanche_sizes))

plt.figure()
bins = np.logspace(0, np.log10(max(avalanche_sizes)+1), 50)
plt.hist(avalanche_sizes, bins=bins)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Avalanche size (number of topplings)')
plt.ylabel('Number of avalanches')
plt.title('Avalanche Size Distribution')
plt.show()

plt.figure()
plt.imshow(grid, cmap='viridis')
plt.colorbar()
plt.title('Final Sandpile Configuration')
plt.show()