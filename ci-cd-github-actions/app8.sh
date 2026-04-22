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
    --acceptance-test-id acceptance-1 \
    --candidate-instance-id staging \
    --baseline-instance-id production \
    --metrics "$METRIC" \
    --input-set-id input-set-1
