import os
from datetime import datetime, timedelta, timezone

import nextmv
from nextmv import cloud

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application(client=client, id="test-highs-app")

# Create the input set.
input_set = cloud_app.new_input_set(
    instance_id="latest",
    start_time=datetime.now(timezone.utc) - timedelta(days=1),
    end_time=datetime.now(timezone.utc),
)
nextmv.write(input_set)
