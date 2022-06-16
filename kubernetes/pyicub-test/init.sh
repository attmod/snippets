#!/bin/bash

# this is a placeholder for all the operations anyone
# would like to do before actually launching python script

source /usr/local/share/robotology-superbuild/setup.sh
yarp detect --write

ICUB_SIMULATION=YES python3 /workdir/script1.py
