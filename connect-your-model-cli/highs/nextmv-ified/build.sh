#!/bin/bash

set -euo pipefail

# Build the Docker image
docker buildx build -f Dockerfile -t highs-solver --platform linux/arm64 --load .

# Extract the compiled binary from the container
docker run --name highs-solver --platform linux/arm64 highs-solver
docker cp highs-solver:/app/main ./main
echo "🐰 Binary extracted to ./main"
mkdir -p HiGHS/build
docker cp highs-solver:/app/HiGHS/build/lib ./HiGHS/build
echo "🐰 Required libraries extracted to ./HiGHS/build/lib"
docker rm highs-solver
echo "🐰 Build completed successfully."
