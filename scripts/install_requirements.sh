#!/bin/bash

home="/home/hp/Desktop/CRUD-Master/srcs"

services=( "/api-gateway-app" "/billing-app" "/inventory-app" )

for d in "${services[@]}"; do
 
cd $home$d

python3 -m venv envs

source ./envs/activate

pip install -r requirements.txt

deactivate
done