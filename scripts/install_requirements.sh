#!/bin/bash

# Get the absolute path of the directory where this script resides
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Define the source directory relative to the script location (parent folder/srcs)
BASE_SRCS_DIR="$(dirname "$SCRIPT_DIR")/srcs"

services=( "api-gateway-app" "billing-app" "inventory-app" )

for d in "${services[@]}"; do

cd "$BASE_SRCS_DIR/$d" || { echo "Directory $d not found"; continue; }

python3 -m venv envs

source ./envs/bin/activate

pip install -r requirements.txt

deactivate
done