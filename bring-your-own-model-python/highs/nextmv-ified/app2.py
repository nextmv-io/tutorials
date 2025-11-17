import nextmv
from nextmv import local

# Instantiate the local application.
local_app = local.Application(src=".")

# Start a new run, loading the file from a directory, and poll for results.
run_results_2 = local_app.new_run_with_result(
    input_dir_path="./inputs",
    output_dir_path="./outputs",
)
nextmv.write(run_results_2)  # This time, print both metadata and output at once.

run_logs_2 = local_app.run_logs(run_id=run_results_2.id)
print(run_logs_2)
