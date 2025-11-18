import os

import nextmv
from nextmv import local

# Instantiate the local application.
local_app = local.Application(src=".")

# Provide any input you want for the app. This input can come from a file, for
# example.
input = nextmv.load(path=os.path.join("inputs", "input.json"))

# Start a new run and get its result immediately.
result_3 = local_app.new_run_with_result(input=input)
nextmv.write(result_3)
