import os

import nextmv
from nextmv import cloud

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application.new(client=client, id="test-highs-app")

# Run the app.
run_result = cloud_app.new_run_with_result(
    input_dir_path="./inputs",  # Data is loaded from a dir.
    run_options={"duration": "3"},
)
nextmv.write(run_result)
