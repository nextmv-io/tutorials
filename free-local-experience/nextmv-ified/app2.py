import nextmv
from nextmv import local

# Instantiate the local application.
local_app = local.Application(src=".")

# Get the result of a specific run by its ID.
result_1 = local_app.run_result(run_id="<RUN_ID_1_PRINTED_IN_STEP_5>")
nextmv.write(result_1)
