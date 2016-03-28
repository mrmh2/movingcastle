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
