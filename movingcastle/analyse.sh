#!/bin/bash

ARGS=$@
PWD=`pwd`

docker run --rm \
-v `pwd`/../movingcastle:/movingcastle \
-v /var/run/docker.sock:/var/run/docker.sock \
movingcastle /movingcastle/calcifer.py analyse $PWD $@
