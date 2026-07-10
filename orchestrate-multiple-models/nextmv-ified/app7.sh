nextmv cloud secrets create -a test-avocado-workflow \
    --secrets '{"type": "env", "location": "NEXTMV_API_KEY", "value": "'"${NEXTMV_API_KEY}"'"}'
