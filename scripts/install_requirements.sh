#!/bin/bash

home="/home/isayen/Desktop/CRUD-Master/srcs"

services=( "/api-gateway-app" "/billing-app" "/inventory-app" )

for d in "${services[@]}"; do
 
cd $home$d

python3 -m venv envs

source ./envs/bin/activate

pip install -r requirements.txt

deactivate
done