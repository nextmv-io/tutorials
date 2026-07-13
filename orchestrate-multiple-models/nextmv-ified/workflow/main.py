import json
import os
import shutil
from typing import Any

import nextmv
import pandas as pd
from nextmv import cloud
from nextpipe import FlowSpec, app, needs, step


class Workflow(FlowSpec):
    @step
    def prepare_regression_data(input: dict[str, Any]) -> str:
        """Prepares the data for the regression model."""

        # dataset downloaded directly from HAB
        avocado = pd.read_csv(input["avocado_data_path"])
        # dataset downloaded from Kaggle
        avocado_old = pd.read_csv(input["avocado_old_data_path"])

        avocado = pd.concat([avocado, avocado_old], ignore_index=True)

        # Save to inputs.
        inputs_dir = "workflow_inputs"
        os.makedirs(inputs_dir, exist_ok=True)
        avocado.to_csv(os.path.join(inputs_dir, "avocado.csv"), index=False)
        with open(os.path.join(inputs_dir, "input.json"), "w") as f:
            json.dump(input, f)

        return inputs_dir

    @app(app_id="test-avocado-regression")
    @needs(predecessors=[prepare_regression_data])
    @step
    def regression() -> None:
        """Runs the regression model."""
        pass

    @needs(predecessors=[prepare_regression_data, regression])
    @step
    def prepare_decision_data(
        workflow_inputs_path: str,
        regression_results_path: str,
    ) -> str:
        """
        Prepares the data for the decision model, after completing the
        regression model.
        """

        # Copy regression coefficients to decision inputs
        decision_inputs_dir = "decision_inputs"
        os.makedirs(decision_inputs_dir, exist_ok=True)

        coeff_file = "coefficients.json"
        shutil.copy(
            os.path.join(regression_results_path, f"{coeff_file}"),
            os.path.join(decision_inputs_dir, coeff_file),
        )

        avo_file = "avocado.csv"
        shutil.copy(
            os.path.join(workflow_inputs_path, avo_file),
            os.path.join(decision_inputs_dir, avo_file),
        )

        input_file = "input.json"
        shutil.copy(
            os.path.join(workflow_inputs_path, input_file),
            os.path.join(decision_inputs_dir, input_file),
        )

        return decision_inputs_dir

    @app(app_id="test-avocado-decision", full_result=True)
    @needs(predecessors=[prepare_decision_data])
    @step
    def decision() -> None:
        """Runs the decision model."""
        pass

    @needs(predecessors=[decision])
    @step
    def resolve_output(result: nextmv.RunResult) -> dict[str, Any]:
        """Writes the final output of the workflow."""

        # Extract the path to the output files.
        result_path = result.output
        # Simply copy the files from the given directory to the expected output
        # directory.
        outputs_dir = "outputs"
        os.makedirs(outputs_dir, exist_ok=True)
        for file_name in os.listdir(result_path):
            full_file_name = os.path.join(result_path, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, outputs_dir)

        metrics = {"metrics": result.metadata.metrics}

        solution_file = "solution.json"
        with open(os.path.join(outputs_dir, solution_file), "r") as f:
            solution_data = json.load(f)

        consolidated_output = {**solution_data, **metrics}

        return consolidated_output


def main():
    """Runs the workflow."""

    # Load input data
    input = nextmv.load()

    # Run workflow
    client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
    workflow = Workflow(name="DecisionWorkflow", input=input.data, client=client)
    workflow.run()

    # Write the result
    result = workflow.get_result(workflow.resolve_output)
    nextmv.write(result)


if __name__ == "__main__":
    main()
