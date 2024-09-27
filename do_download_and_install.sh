#!/bin/bash

container_name='docker-database-server'
repo_name='docker-database-server'

# Function to check if Docker container is running
container_running() {
    docker ps --filter "name=$container_name" --format '{{.Names}}' | grep -q "$container_name"
}

# Check if the container already exists
if docker ps -a --format '{{.Names}}' | grep -q $container_name; then
    echo "Container '$container_name' already exists."
    CONTAINER_ID=$(docker ps -aqf "name=$container_name")

    if [ "$(docker inspect --format '{{.State.Status}}' $CONTAINER_ID)" == "running" ]; then
        echo "Container is running, using the existing container..."
    else
        echo "Container is not running, starting it..."
        docker start $container_name
        sleep 20
    fi
else
    echo "Container '$container_name' does not exist, creating it..."
    CONTAINER_ID=$(docker run --rm -d --name $container_name --privileged --entrypoint /bin/bash arm32v7/ubuntu:latest)
    echo "Container ID after creation: $CONTAINER_ID"
    sleep 20
fi

# Verify the container exists and is running
if docker ps -a --format '{{.Names}}' | grep -q $container_name; then
    echo "** Container '$container_name' exists and is ready. Proceeding with package installation..."

    # Install necessary packages
    docker exec $container_name bash -c 'which node npm python3 pip3 tsc curl wget' > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Installing necessary packages..."
        docker exec $container_name apt-get install -y python3
