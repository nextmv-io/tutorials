import os

from nextmv import cloud

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application.new(
    client=client,
    name="test-highs-app",
    id="test-highs-app",
    exist_ok=True,
)
print("Cloud application created:", cloud_app.id)
