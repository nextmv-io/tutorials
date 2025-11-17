import os

from nextmv import cloud, local

# Instantiate the local application.
local_app = local.Application(src=".")

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application.new(
    client=client,
    name="test-pyomo-app",
    id="test-pyomo-app",
    exist_ok=True,
)

# Sync the local app's runs to the cloud app.
local_app.sync(target=cloud_app, verbose=True)
