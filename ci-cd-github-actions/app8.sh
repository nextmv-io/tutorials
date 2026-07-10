METRIC='{
    "field": "result.value",
    "metric_type": "direct-comparison",
    "params": {
        "operator": "le",
        "tolerance": {"type": "relative", "value": 0.05}
    },
    "statistic": "mean"
}'
nextmv cloud acceptance create --app-id nextroute \
    --candidate-instance-id staging \
    --baseline-instance-id production \
    --metrics "$METRIC" \
    --input-set-id "<INPUT_SET_ID_CREATED_IN_LAST_STEP>"
