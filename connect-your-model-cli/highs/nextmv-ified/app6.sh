SCENARIO='{
    "instance_id": "latest",
    "scenario_input": {
        "scenario_input_type": "input_set",
        "scenario_input_data": "<INPUT_SET_ID_CREATED_IN_LAST_STEP>"
    },
    "configuration": [
        {
            "name": "duration",
            "values": ["1", "3", "5"]
        }
    ]
}'
nextmv cloud scenario create -a test-highs -r 2 --scenarios "$SCENARIO"
