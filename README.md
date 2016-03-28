docker run --name some-redis -d redis

## Data staging

Managed by dataprocessor container which is:

* Mounted with /data for it to stage into

mkdir yeast_growth
cd yeast_growth
git clone git@github.com:JIC-Image-Analysis/yeast_growth code
mkdir data
mkdir output
mkdir working

gsutil cp gs://data-repo/yeast_growth/* .

docker run -it --rm

docker run -it --rm -v `pwd`/code:/code -v `pwd`/data:/data -v `pwd`/output:/output jicscicomp/jicbioimage


## TODO

Add docker to movingcastle container

docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v `pwd`:/project movingcastl


```analyse.sh
#!/bin/bash

ARGS=$@
PWD=`pwd`

echo $ARGS $PWD```