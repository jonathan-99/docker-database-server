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
        docker exec $container_name apt-get install -y python3 python3-pip curl wget
        docker exec $container_name apt-get install -y --upgrade setuptools
    else
        echo "Necessary packages are already installed."
    fi

    # Update and upgrade packages
    docker exec $container_name apt-get update -y
    docker exec $container_name apt-get upgrade -y

    # Remove repository if already cloned
    if docker exec $container_name ls $repo_name &> /dev/null; then
        echo "Repository already exists in the container. Removing..."
        docker exec $container_name rm -rf $repo_name
    fi

    # Clone repository
    echo "Cloning repository..."
    docker exec $container_name git clone https://github.com/jonathan-99/$repo_name.git $repo_name

    # Display various information
    echo "OS Version:"
    docker exec $container_name cat /etc/os-release

    echo "Python Version:"
    docker exec $container_name python3 --version

    echo "Unittest Version:"
    docker exec $container_name python3 -m unittest

    echo "Coverage Version:"
    docker exec $container_name coverage --version

    echo "Docker Image ID:"
    docker exec $container_name cat /proc/self/cgroup | grep "docker" | sed 's/^.*\///' | head -n 1

else
    echo "Error: Container does not exist. Exiting."
    exit 1
fi
