import random

rows = int(random.randint(3, 10))

grid = [[0 for _ in range(rows)] for _ in range(rows)]
x = 0
y = 0
n_obst = rows - 2
while(n_obst > 0):
    x = random.randint(1, rows-1)
    y = random.randint(1, rows-1)
    if(grid[x][y] < 1):
        grid[x][y] = 1
        n_obst = n_obst - 1

sinal = 0
while(sinal < 1):
    x = random.randint(1, rows-1)
    y = random.randint(1, rows-1)
    if(grid[x][y]<1):
        grid[x][y] = 2
        sinal = 1                 
                   
for row in grid:
    print(row)        