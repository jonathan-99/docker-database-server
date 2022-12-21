#!/bin/bash

set -eu -o pipefail # fail on error and report it, debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo privilege to run this script"

# Modify how the shell environment operates
# Terminate whenever an error occurs (e.g., command not found)
# If a variable does not exist, report the error and stop (e.g., unbound variable)
# If a sub-command fails, the entire pipeline command fails, terminating the script (e.g., command not found)

echo installing the must-have pre-requisites
while read -r p ; do sudo "$p" -y ; done < <(cat << "EOF"
    apt-get update
    apt-get upgrade
    pip3 install --upgrade setuptools
    pip3 install docker
    pip3 install mysql-connector-python
    pip3 install flask
EOF
)

export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

echo installing the nice-to-have pre-requisites
echo you have 5 seconds to proceed ...
echo or
echo hit Ctrl+C to quit
echo -e "\n"
sleep 6

sudo apt-get install -y tig