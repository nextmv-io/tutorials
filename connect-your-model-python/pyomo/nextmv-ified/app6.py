import os

import nextmv
from nextmv import cloud

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application(client=client, id="test-pyomo-app")

# Run the app.
input = nextmv.load(path=os.path.join("inputs", "problem.json"))
run_result = cloud_app.new_run_with_result(
    input=input.data,  # Data is loaded from memory.
    run_options={
        "duration": "3",
        "solver": "scip",
    },
)
nextmv.write(run_result)
