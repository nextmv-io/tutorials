import os

import nextmv
from nextmv import cloud

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application.new(
    client=client,
    name="test-highs-app",
    id="test-highs-app",
    exist_ok=True,
)

# Run the app.
run_result = cloud_app.new_run_with_result(
    input_dir_path="./inputs",  # Data is loaded from a dir.
    run_options={"duration": "3"},
)
nextmv.write(run_result)
