#!/bin/bash

ARGS=$@
PWD=`pwd`

docker run --rm \
-it \
-v `pwd`/../movingcastle:/movingcastle \
-v /var/run/docker.sock:/var/run/docker.sock \
movingcastle
