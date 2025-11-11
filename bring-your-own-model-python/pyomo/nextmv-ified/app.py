import os
import time

import nextmv
from nextmv import cloud, local

# Instantiate the local app.
local_app = local.Application(src=".")

# Start a new run, load the data from a file.
problem = nextmv.load(path=os.path.join("inputs", "problem.json"))
run_id_1 = local_app.new_run(input=problem.data)

# Sleep and get metadata, output (results), logs.
time.sleep(3)

run_metadata_1 = local_app.run_metadata(run_id=run_id_1)
nextmv.write(run_metadata_1)

run_results_1 = local_app.run_result(run_id=run_id_1)
nextmv.write(run_results_1.output)

run_logs_1 = local_app.run_logs(run_id=run_id_1)
print(run_logs_1)

# Start a new run, and poll for results.
run_results_2 = local_app.new_run_with_result(input=problem.data)
nextmv.write(run_results_2)  # This time, print both metadata and output at once.

run_logs_2 = local_app.run_logs(run_id=run_results_2.id)
print(run_logs_2)

# Instantiate the cloud app.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application.new(
    client=client,
    name="test-pyomo-app",
    id="test-pyomo-app",
    exist_ok=True,
)

# Sync the local app's runs to the cloud app.
local_app.sync(target=cloud_app, verbose=True)

# Push the app.
manifest = nextmv.Manifest.from_yaml(dirpath=".")
cloud_app.push(manifest=manifest, app_dir=".", verbose=True)
