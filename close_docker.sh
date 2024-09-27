#!/bin/bash


set -euo pipefail

# Check for sudo privileges
sudo -n true
if [ $? -ne 0 ]; then
    echo "You should have sudo privilege to run this script."
    exit 1
fi

container_name='docker-database-server'

# Stop and remove the Docker container if it exists
if docker ps -a --format '{{.Names}}' | grep -q $container_name; then
    echo "Stopping and removing container '$container_name'..."
    docker stop $container_name
    docker rm $container_name
else
    echo "Container '$container_name' is not running."
fi