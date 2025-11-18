import nextmv
from nextmv import local

# Instantiate the local application.
local_app = local.Application(src=".")

# Get the information of a specific run by its ID.
result_info_2 = local_app.run_metadata(run_id="<RUN_ID_2_PRINTED_IN_STEP_5>")
nextmv.write(result_info_2)
