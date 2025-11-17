import os
import time

import nextmv
from nextmv import local

# Instantiate the local application.
local_app = local.Application(src=".")

# Provide any input you want for the app. This input can come from a file, for
# example.
problem = nextmv.load(path=os.path.join("inputs", "problem.json"))
run_id_1 = local_app.new_run(input=problem.data)

# Sleep and get metadata, output (results), logs.
time.sleep(5)

run_metadata_1 = local_app.run_metadata(run_id=run_id_1)
nextmv.write(run_metadata_1)

run_results_1 = local_app.run_result(run_id=run_id_1)
nextmv.write(run_results_1.output)

run_logs_1 = local_app.run_logs(run_id=run_id_1)
print(run_logs_1)
