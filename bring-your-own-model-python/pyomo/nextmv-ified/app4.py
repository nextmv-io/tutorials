import os

import nextmv
from nextmv import cloud

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application.new(
    client=client,
    name="test-pyomo-app",
    id="test-pyomo-app",
    exist_ok=True,
)

# Push the app.
manifest = nextmv.Manifest.from_yaml(dirpath=".")
cloud_app.push(manifest=manifest, app_dir=".", verbose=True)
