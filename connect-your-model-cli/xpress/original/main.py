import xpress as xp

q = 3

starting_grid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
]

n = q**2  # the size must be the square of the size of the subgrids
N = range(n)

p = xp.problem()

x = p.addVariables(N, N, N, vartype=xp.binary)

# define all q^2 subgrids
subgrids = {
    (h, l): [(i, j) for i in range(q * h, q * h + q) for j in range(q * l, q * l + q)]
    for h in range(q)
    for l in range(q)
}

vertical = [xp.Sum(x[i, j, k] for i in N) == 1 for j in N for k in N]
horizontal = [xp.Sum(x[i, j, k] for j in N) == 1 for i in N for k in N]
subgrid = [
    xp.Sum(x[i, j, k] for (i, j) in subgrids[h, l]) == 1
    for (h, l) in subgrids.keys()
    for k in N
]

# Assign exactly one number to each cell

assign = [xp.Sum(x[i, j, k] for k in N) == 1 for i in N for j in N]

init = [
    x[i, j, k] == 1 for k in N for i in N for j in N if starting_grid[i][j] == k + 1
]

p.addConstraint(vertical, horizontal, subgrid, assign, init)

p.optimize()

print("Solution:")

for i in N:
    for j in N:
        l = [k for k in N if p.getSolution(x[i, j, k]) >= 0.5]
        assert len(l) == 1
        print("{0:2d}".format(1 + l[0]), end="", sep="")
    print("")
