#!/bin/bash

ARGS=$@
PWD=`pwd`
CONTAINER=movingcastle

if [ ! -d "movingcastle" ]; then
    docker run --rm \
    -v `pwd`:/deploy \
    $CONTAINER \
    git clone https://github.com/mrmh2/movingcastle /deploy/movingcastle
fi

docker run --rm \
-v `pwd`:/deploy \
-v /var/run/docker.sock:/var/run/docker.sock \
-v `pwd`/movingcastle/movingcastle:/movingcastle \
$CONTAINER \
/movingcastle/calcifer.py deploy
