import nextmv
import xpress as xp

input = nextmv.load()
q = input.data["q"]
starting_grid = input.data["starting_grid"]

n = q**2  # the size must be the square of the size of the subgrids
N = range(n)

nextmv.redirect_stdout()  # Solver chatter is logged to stderr.

p = xp.problem()
p.setControl("timelimit", input.options.duration)

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
solution = {}
rows = []
for i in N:
    row = []
    for j in N:
        l = [k for k in N if p.getSolution(x[i, j, k]) >= 0.5]
        assert len(l) == 1
        value = 1 + l[0]
        row.append(value)
        print("{0:2d}".format(value), end="", sep="")
    rows.append(row)
    print("")

for i, row in enumerate(rows):
    solution[f"row_{i}"] = row

metrics = {
    "duration": p.attributes.time,
    "objective": p.attributes.objval,
    "num_variables": p.attributes.cols,
    "num_constraints": p.attributes.rows,
}

nextmv.write(solution=solution, metrics=metrics, options=input.options)
