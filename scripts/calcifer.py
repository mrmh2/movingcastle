#!/usr/bin/env python

import os
import errno
import subprocess

import yaml

from docklet import DockerBroker

from datastager import DataStager

# docker run -it --rm -v ~/projects/calcifer/resources/:/root datamangler
# gsutil config -e
# mserviceaccount@mhelloworld-1228.iam.gserviceaccount.com

HERE = os.path.dirname(__file__)
DOCKERFILES = os.path.join(HERE, '..', 'dockerfiles')

def mkdir_p(path):
    try:
        os.makedirs(path)   
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

class Project(object):

    def __init__(self, project_filename):
        with open(project_filename) as f:
            yaml_data = yaml.load(f)

        self.name = yaml_data['name']
        self.data_repo = yaml_data['data_repo']


class Node(object):

    pass

class Analysis(object):

    def __init__(self, project, filename):
        self.setup_paths()

        self.filename = filename

        self.data_repo = project.data_repo

    def setup_paths(self):
        mkdir_p(self.raw_path)

    @property
    def working(self):
        return os.path.join(HERE, '..', 'working')

    @property
    def raw_path(self):
        return os.path.join(self.working, 'raw')

    def stage_data(self):

        if not len(os.listdir(self.raw_path)):
            ds = DataStager(self.data_repo, self.raw_path)

            ds.stage_file(self.filename)


def build_container(container_name, docker_file_path):

    full_docker_path = os.path.join(DOCKERFILES, docker_file_path)

    command = ('docker',
               'build',
               '-t',
               container_name,
               full_docker_path)

    print ' '.join(command)

    subprocess.call(command)

def build_containers():
    build_container('datamangler', 'datamangler')

def create_data_volume(volume_name, mount_point):
    
    command = ('docker',
               'create',
               '-v',
               mount_point,
               '--name',
               volume_name,
               'centos',
               '/bin/true')

    print ' '.join(command)

    subprocess.call(command)


def create_data_volumes():
    create_data_volume('working', '/working')
    create_data_volume('raw_data', '/raw_data')

def main():

    db = DockerBroker()


    myproj = Project('project.yml')
    an = Analysis(myproj, "C0000230.ISQ")

    an.stage_data()

    #print db.list_images()
    #build_containers()
    #create_data_volumes()

if __name__ == "__main__":
    main()
