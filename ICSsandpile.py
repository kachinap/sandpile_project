import numpy as np
import matplotlib.pyplot as plt

N=200 #gridsize
K=3 #slope at critical point

def initialize_grid():
    grid = np.zeros((N,N))
    grid[1:-1,1:-1] = 7 #non-border cells slope of 7>K
    return grid

def tumble(grid):
    gridchanges=np.zeros((N,N))
    tumbled=False
    for i in range(1,N-1):
        for j in range(1,N-1):
            if grid[i,j] >= K:
                gridchanges[i,j] -= 4
                gridchanges[i+1,j] += 1
                gridchanges[i-1,j] += 1
                gridchanges[i,j+1] += 1
                gridchanges[i,j-1] += 1
                tumbled=True
    grid += gridchanges

