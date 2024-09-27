#!/bin/bash


set -euo pipefail

# Check for sudo privileges
sudo -n true
if [ $? -ne 0 ]; then
    echo "You should have sudo privilege to run this script."
    exit 1
fi

container_name='docker-database-server'

#!/bin/bash

container_name='docker-database-server'
log_file="/var/lib/jenkins/workspace/docker-database-server/test_output.log"

# Create or clear the log file
> $log_file

# Stop and remove the Docker container if it exists
if docker ps -a --format '{{.Names}}' | grep -q $container_name; then
    echo "Stopping and removing container '$container_name'..." | tee -a $log_file
    docker stop $container_name | tee -a $log_file
    docker rm $container_name | tee -a $log_file

    echo "Running tests and logging output..." | tee -a $log_file

    # Run unittests and capture the output
    docker exec $container_name python3 -m unittest discover -s /path/to/tests -p '*.py' | tee -a $log_file

    # Optionally run other tests or commands and capture their output
    docker exec $container_name python3 --version | tee -a $log_file
    docker exec $container_name coverage --version | tee -a $log_file

else
    echo "Container '$container_name' is not running." | tee -a $log_file
fi
