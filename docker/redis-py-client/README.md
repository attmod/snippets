# Setup

.env file controls filenames and docker source image

Needs port :10000 for yarpserver

# Building

Requires access to docker hub
    make build

TODO: minimal image based on ubuntu + yarp essentials

# Start

Will run in detached mode
    make run

# Stop

Stop the container running in the background
    make stop