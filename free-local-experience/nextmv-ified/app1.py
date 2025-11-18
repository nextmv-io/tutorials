import os

import nextmv
from nextmv import local

# Instantiate the local application.
local_app = local.Application(src=".")

# Provide any input you want for the app. This input can come from a file, for
# example.
input = nextmv.load(path=os.path.join("inputs", "input.json"))

# Execute some local runs with the provided input.
run_1 = local_app.new_run(input=input)
print("run_1:", run_1)

run_2 = local_app.new_run(input=input)
print("run_2:", run_2)
