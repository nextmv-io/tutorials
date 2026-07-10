import json
import time
from importlib.metadata import version
from typing import Any

import highspy
import nextmv
import plotly.graph_objects as go


def main() -> None:
    """Entry point for the program."""

    loaded_input = nextmv.load()
    options = loaded_input.options

    nextmv.log("Solving knapsack problem:")
    nextmv.log(f"  - items: {len(loaded_input.data.get('items', []))}")
    nextmv.log(f"  - capacity: {loaded_input.data.get('weight_capacity', 0)}")

    solution, metrics, assets = solve(loaded_input)
    nextmv.write(solution=solution, metrics=metrics, assets=assets, options=options)


def solve(
    loaded_input: nextmv.Input,
) -> tuple[dict[str, Any], dict[str, Any], list[nextmv.Asset]]:
    """Solves the given problem and returns the solution, metrics, and assets."""

    start_time = time.time()

    # Creates the solver.
    solver = highspy.Highs()
    solver.silent()  # Solver output ignores stdout redirect, silence it.
    solver.setOptionValue("time_limit", loaded_input.options.duration)

    # Initializes the linear sums.
    weights = 0.0
    values = 0.0

    # Creates the decision variables and adds them to the linear sums.
    items = []
    for item in loaded_input.data["items"]:
        item_variable = solver.addVariable(0.0, 1.0, item["value"])
        items.append({"item": item, "variable": item_variable})
        weights += item_variable * item["weight"]
        values += item_variable * item["value"]

    # This constraint ensures the weight capacity of the knapsack will not be
    # exceeded.
    solver.addConstr(weights <= loaded_input.data["weight_capacity"])

    # Sets the objective function: maximize the value of the chosen items.
    status = solver.maximize(values)

    # Determines which items were chosen.
    chosen_items = [
        item["item"] for item in items if solver.val(item["variable"]) > 0.9
    ]

    solution = {"items": chosen_items}

    metrics = {
        "duration": time.time() - start_time,
        "value": sum(item["value"] for item in chosen_items),
        "status": str(status),
        "variables": solver.numVariables,
        "constraints": solver.numConstrs,
        "solver_version": version("highspy"),
    }

    # After solving, create visualization.
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[item["id"] for item in chosen_items],
            y=[item["value"] for item in chosen_items],
            name="Value",
        )
    )
    fig.add_trace(
        go.Bar(
            x=[item["id"] for item in chosen_items],
            y=[item["weight"] for item in chosen_items],
            name="Weight",
        )
    )
    fig.update_layout(
        title="Selected Items: Value vs Weight",
        barmode="group",
    )

    assets = [
        nextmv.Asset(
            name="item-chart",
            content=[json.loads(fig.to_json())],
            visual=nextmv.Visual(
                visual_schema=nextmv.VisualSchema.PLOTLY,
                label="Item Analysis",
            ),
        )
    ]

    return solution, metrics, assets


if __name__ == "__main__":
    main()
