#!/bin/bash


set -euo pipefail

# Check for sudo privileges
sudo -n true
if [ $? -ne 0 ]; then
    echo "You should have sudo privilege to run this script."
    exit 1
fi

# Define container name
container_name='docker-database-server'

# Stop the Docker container
if [ -n "$(docker ps -q --filter "name=${container_name}")" ]; then
    docker stop ${container_name}
    echo "Docker container '${container_name}' stopped."
else
    echo "Docker container '${container_name}' is not running."
fi