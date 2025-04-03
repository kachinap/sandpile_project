import numpy as np
import matplotlib.pyplot as plt

N = 50           # gridsize
K = 3            # slope at critical point
V = 7            # initial slope of interior cells 
num_examples = 3  # number of separate avalanche examples

# for reproducibility of random positions:
np.random.seed(42)

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

# initialize grid and reach equilibrium
print("Initializing grid...")
initial_grid = initialize_grid()
critical_state = run_to_equilibrium(initial_grid)

fig, axes = plt.subplots(1, num_examples, figsize=(5 * num_examples, 5))

for ex in range(num_examples):
    current_grid = critical_state.copy()

    i = np.random.randint(1, N-1)
    j = np.random.randint(1, N-1)
    print(f"\nExample {ex+1}: Adding grain at ({i}, {j})")
    current_grid[i, j] += 1

    avalanche_size, final_grid = run_avalanche(current_grid)
    print(f"Avalanche size for example {ex+1}: {avalanche_size}")

    ax = axes[ex] if num_examples > 1 else axes
    im = ax.imshow(final_grid, cmap='viridis', interpolation='nearest')
    ax.set_title(f"Example {ex+1}\nGrain at ({i},{j}), Size={avalanche_size}")
    plt.colorbar(im, ax=ax)

plt.tight_layout()
plt.show()