#!/bin/bash

ARGS=$@
PWD=`pwd`
CONTAINER=jicscicomp/movingcastle

docker run --rm \
-v `pwd`/../movingcastle/movingcastle:/movingcastle \
-v /var/run/docker.sock:/var/run/docker.sock \
$CONTAINER \
/movingcastle/calcifer.py analyse $PWD $@
