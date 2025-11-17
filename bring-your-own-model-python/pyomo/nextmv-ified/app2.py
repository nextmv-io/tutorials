import os

import nextmv
from nextmv import local

# Instantiate the local application.
local_app = local.Application(src=".")

# Start a new run, loading the data from a file, and poll for results.
problem = nextmv.load(path=os.path.join("inputs", "problem.json"))
run_results_2 = local_app.new_run_with_result(input=problem.data)
nextmv.write(run_results_2)  # This time, print both metadata and output at once.

run_logs_2 = local_app.run_logs(run_id=run_results_2.id)
print(run_logs_2)
