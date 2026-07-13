SCENARIO='{
    "instance_id": "latest",
    "scenario_input": {
        "scenario_input_type": "input_set",
        "scenario_input_data": "<INPUT_SET_ID_CREATED_PREVIOUSLY>"
    },
    "configuration": [
        {
            "name": "vehicle_maximum_travel_distance",
            "values": ["3000", "2500", "2000"]
        },
        {
            "name": "global_span_cost_coefficient",
            "values": ["100", "1000"]
        }
    ]
}'
nextmv cloud scenario create -a test-ortools --scenarios "$SCENARIO"
