import numpy as np
import matplotlib.pyplot as plt

N = 200          # gridsize
K = 3            # slope at critical point
V = 7            # initial slope of interior cells
num_iterations = 5000  # number of grains to add

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

def simulate_sandpile():
    # main loop: add one grain and let the system relax
    grid=initialize_grid()
    avalanche_sizes = []  # to record the number of topplings per avalanche
    for it in range(num_iterations):
        # add a grain to a random interior cell
        i = np.random.randint(1, N-1)
        j = np.random.randint(1, N-1)
        grid[i, j] += 1
        avalanche = run_avalanche(grid)
        avalanche_sizes.append(avalanche)
    return (grid, avalanche_sizes)


# run simulation
grid,avalanche_sizes = simulate_sandpile()
print("Simulation complete")
print("Average avalanche size:", np.mean(avalanche_sizes))
print("Max avalanche size:", np.max(avalanche_sizes))
plt.figure()
plt.imshow(grid, cmap='viridis')
plt.colorbar()
plt.title('Final Sandpile Configuration')
plt.show()


plt.figure()
bins = np.logspace(0, np.log10(max(avalanche_sizes)+1), 50)
plt.hist(avalanche_sizes, bins=bins)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Avalanche size (number of topplings)')
plt.ylabel('Number of avalanches')
plt.title('Avalanche Size Distribution')
plt.show()

