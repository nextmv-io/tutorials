import os

from nextmv import cloud

# Instantiate the cloud application.
client = cloud.Client(api_key=os.getenv("NEXTMV_API_KEY"))
cloud_app = cloud.Application(client=client, id="test-pyomo-app")

# Create the scenario test.
scenario_test_id = cloud_app.new_scenario_test(
    scenarios=[
        cloud.Scenario(
            scenario_input=cloud.ScenarioInput(
                scenario_input_type=cloud.ScenarioInputType.INPUT_SET,
                scenario_input_data="input-set-2",
            ),
            instance_id="latest",
            configuration=[
                cloud.ScenarioConfiguration(
                    name="duration",
                    values=["1", "3", "5"],
                ),
                cloud.ScenarioConfiguration(
                    name="solver",
                    values=["glpk", "scip", "cbc"],
                ),
            ],
        ),
    ],
)
print(f"Created scenario test with ID: {scenario_test_id}")
