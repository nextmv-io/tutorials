# Example of a shortest path network flow in a graph
# Shows integration of highspy with networkx

import highspy
import networkx as nx
import nextmv

nextmv.redirect_stdout()
input = nextmv.load(
    data_files=[
        nextmv.json_data_file("nodes", input_data_key="nodes"),
        nextmv.csv_data_file("edges", input_data_key="edges"),
    ],
)
options = input.options

nodes = input.data["nodes"]
orig, dest = (nodes["origin"], nodes["destination"])

# create directed graph with edge weights (distances)
G = nx.DiGraph()
G.add_weighted_edges_from(
    [(edge["from"], edge["to"], float(edge["weight"])) for edge in input.data["edges"]]
)

h = highspy.Highs()
h.setOptionValue("time_limit", options.duration)

x = h.addBinaries(G.edges, obj=nx.get_edge_attributes(G, "weight"))

# add flow conservation constraints
#                        {  1  if n = orig
#   sum(out) - sum(in) = { -1  if n = dest
#                        {  0     otherwise
rhs = lambda n: 1 if n == orig else -1 if n == dest else 0
flow = lambda E: h.qsum((x[e] for e in E))

h.addConstrs(flow(G.out_edges(n)) - flow(G.in_edges(n)) == rhs(n) for n in G.nodes)
h.minimize()

# Print the solution
shortest_path = []
print("Shortest path from", orig, "to", dest, "is: ", end="")
sol = h.vals(x)

n = orig
while n != dest:
    shortest_path.append(n)
    print(n, end=" ")
    n = next(e[1] for e in G.out_edges(n) if sol[e] > 0.5)

print(dest)

solution = {"shortest_path": shortest_path}
metrics = {
    "duration": h.getRunTime(),
    "value": h.getInfo().objective_function_value,
    "variables": h.numVariables,
    "constraints": h.numConstrs,
    "length_shortest_path": len(shortest_path),
}
nextmv.write(
    options=options,
    metrics=metrics,
    solution_files=[
        nextmv.json_solution_file(name="shortest_path", data=solution),
    ],
)
