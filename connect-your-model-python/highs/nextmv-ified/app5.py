import os

import nextmv
from nextmv import cloud

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application(client=client, id="test-highs-app")

# Push the app.
manifest = nextmv.Manifest.from_yaml(dirpath=".")
cloud_app.push(manifest=manifest, app_dir=".", verbose=True)
