"""Capacited Vehicles Routing Problem (CVRP)."""

import json

import nextmv
import plotly.graph_objects as go
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def print_solution(
    data,
    manager,
    routing,
    solution,
) -> tuple[list[nextmv.Asset], dict, dict]:
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")

    total_distance = 0
    total_load = 0
    routes = []
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        plan = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
            stop = {
                "node": node_index,
                "load": route_load,
            }
            plan.append(stop)
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        stop = {
            "node": manager.IndexToNode(index),
            "load": route_load,
        }
        plan.append(stop)
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        route = {
            "vehicle_id": vehicle_id,
            "distance": route_distance,
            "load": route_load,
            "plan": plan,
        }
        routes.append(route)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")

    metrics = {
        "duration": routing.solver().WallTime() / 1000.0,
        "value": solution.ObjectiveValue(),
        "total_distance": total_distance,
        "total_load": total_load,
    }

    # Create visualization assets
    assets = create_route_visualization(data, routes)
    solution = {"routes": routes}

    return assets, metrics, solution


def create_route_visualization(data, routes) -> list[nextmv.Asset]:
    """Create a Plotly visualization of the vehicle routes."""
    coordinates = data.get("coordinates", [])
    if not coordinates:
        return []

    fig = go.Figure()

    # Define colors for different vehicles
    colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "gray"]

    # Plot each route
    for route in routes:
        vehicle_id = route["vehicle_id"]
        plan = route["plan"]
        color = colors[vehicle_id % len(colors)]

        # Extract coordinates for this route
        route_x = []
        route_y = []
        for stop in plan:
            node = stop["node"]
            if node < len(coordinates):
                route_x.append(coordinates[node][0])
                route_y.append(coordinates[node][1])

        # Plot the route as a line
        fig.add_trace(
            go.Scatter(
                x=route_x,
                y=route_y,
                mode="lines+markers",
                name=f"Vehicle {vehicle_id}",
                line=dict(color=color, width=2),
                marker=dict(size=8),
            )
        )

    # Highlight the depot
    if coordinates:
        depot_x, depot_y = coordinates[0]
        fig.add_trace(
            go.Scatter(
                x=[depot_x],
                y=[depot_y],
                mode="markers",
                name="Depot",
                marker=dict(size=15, color="black", symbol="star"),
            )
        )

    # Update layout
    fig.update_layout(
        title="CVRP Routes Visualization",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        showlegend=True,
        hovermode="closest",
        yaxis=dict(scaleanchor="x", scaleratio=1),
    )

    # Convert figure to JSON
    fig_json = fig.to_json()

    # Create asset
    assets = [
        nextmv.Asset(
            name="Route Visualization",
            content_type="json",
            visual=nextmv.Visual(
                visual_schema=nextmv.VisualSchema.PLOTLY,
                visual_type="custom-tab",
                label="Routes",
            ),
            content=[json.loads(fig_json)],
        )
    ]

    return assets


def main():
    """Solve the CVRP problem."""
    nextmv.redirect_stdout()
    input = nextmv.load()
    options = input.options

    # Instantiate the data problem.
    data = input.data

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(options.duration)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        assets, metrics, solution = print_solution(data, manager, routing, solution)
        nextmv.write(assets=assets, metrics=metrics, solution=solution, options=options)


if __name__ == "__main__":
    main()
