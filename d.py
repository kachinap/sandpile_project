import numpy as np
import matplotlib.pyplot as plt

N = 50           # gridsize
K = 3            # slope at critical point
V = 7            # initial slope of interior cells 

def initialize_grid():
    # a grid with boundaries fixed at 0 and interior cells set to 7
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
    print("Running to equilibrium...")
    grid = grid.copy()
    iteration = 0
    while True:
        count, grid = topple(grid)
        iteration += 1
        if iteration % 100 == 0:
            print(f"Iteration {iteration}, topplings this round: {count}")
        if count == 0:
            break
    print(f"Reached equilibrium after {iteration} iterations")
    return grid

def run_avalanche(grid):
    print("Starting avalanche...")
    avalanche_size = 0
    iteration = 0
    while True:
        count, grid = topple(grid)
        iteration += 1
        # progress every 100 iterations
        if iteration % 100 == 0:
            print(f"Iteration {iteration}, topplings this round: {count}")
        if count == 0:
            break
        avalanche_size += count
    print(f"Total avalanche iterations: {iteration}")
    return avalanche_size, grid

def add_grain_run_avalanche(grid):
    # add a grain to a random interior cell
    i = np.random.randint(1, N-1)
    j = np.random.randint(1, N-1)
    print(f"Adding grain at position ({i}, {j})")
    grid[i, j] += 1
    return run_avalanche(grid)

# initialize grid and reach equilibrium
print("Initializing grid...")
initial_grid = initialize_grid()
critical_state = run_to_equilibrium(initial_grid)

plt.figure(figsize=(14,7))

# example 1
print("Running example 1...")
critical_state1 = critical_state.copy()
avalanche_size1, final_state1 = add_grain_run_avalanche(critical_state1)
print("Avalanche size for example 1:", avalanche_size1)

plt.subplot(1, 2, 1)
plt.imshow(final_state1, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Height')
plt.title(f"Example 1: {avalanche_size1} topplings")

# Example 2
print("Running example 2...")
critical_state2 = critical_state.copy()
avalanche_size2, final_state2 = add_grain_run_avalanche(critical_state2)
print("Avalanche size for example 2:", avalanche_size2)

plt.subplot(1, 2, 2)
plt.imshow(final_state2, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Height')
plt.title(f"Example 2: {avalanche_size2} topplings")

plt.show()