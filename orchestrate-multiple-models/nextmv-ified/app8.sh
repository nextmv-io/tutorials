# Run this command from the root of the workflow app, this is, where the workflow/app.yaml file is located.
nextmv cloud run create -a test-avocado-workflow -i input.json --secrets "<SECRETS_COLLECTION_ID_CREATED_PREVIOUSLY>"
