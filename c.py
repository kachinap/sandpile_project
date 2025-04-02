import numpy as np
import matplotlib.pyplot as plt

N = 200          # gridsize
K = 3            # slope at critical point
V = 7            # initial slope of interior cells

def initialize_grid():
    # a grid with boundaries fixed at 0 and interior cells set to 7
    grid = np.zeros((N, N), dtype=int)
    grid[1:-1, 1:-1] = V
    return grid

def topple(grid):
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
    return topple_count

def run_avalanche(grid):
    avalanche_size = 0
    iteration = 0
    while True:
        count = topple(grid)
        iteration += 1
        # progress every 100 iterations
        if iteration % 100 == 0:
            print(f"Iteration {iteration}, topplings this round: {count}")
        if count == 0:
            break
        avalanche_size += count
    print(f"Total avalanche iterations: {iteration}")
    return avalanche_size



grid = initialize_grid()

# run the avalanche dynamics until the system relaxes to equilibrium
initial_avalanche = run_avalanche(grid)
print("Avalanche triggered during initial relaxation:", initial_avalanche)

plt.figure(figsize=(6,6))
plt.imshow(grid, cmap='viridis', interpolation='nearest')
plt.colorbar()
plt.title("Equilibrium State of the Sandpile\n(Initial state: zi,j = 7 for interior cells)")
plt.show()