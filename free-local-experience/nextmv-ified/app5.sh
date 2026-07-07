RUN_ID=$(nextmv local run create --input inputs/input_with_coordinates.json --wait | jq -r .id)
nextmv local run visuals -r $RUN_ID
