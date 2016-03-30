#!/usr/bin/env python
"""MovingCastle deploy and setup agent."""

import os
import sys
import errno
import shutil
import argparse
import subprocess

import yaml

from docklet import DockerBroker

from datastager import DataStager

# docker run -it --rm -v ~/projects/calcifer/resources/:/root datamangler
# gsutil config -e
# mserviceaccount@mhelloworld-1228.iam.gserviceaccount.com

HERE = os.path.dirname(os.path.abspath(__file__))
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

        self.container_name = 'imagent'

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

    def start_container(self):

        agent = os.path.join(HERE, '..', 'agent')

        command = ['docker',
                    'run',
                    '--rm',
                    '-v',
                    self.working + ':' + '/working',
                    '-v',
                    agent + ':' + '/agent',
                    self.container_name,
                    '/agent/imagent.py']

        subprocess.call(command)

    def debug_container(self):

        agent = os.path.join(HERE, '..', 'agent')

        command = ['docker',
                    'run',
                    '-it',
                    '--rm',
                    '-v',
                    self.working + ':' + '/working',
                    '-v',
                    agent + ':' + '/agent',
                    '--link',
                    'some-redis:redis',
                    self.container_name]

        subprocess.call(command)      

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

def deploy(args):

    project_name = 'yeast_growth'
    project_url = 'https://github.com/JIC-Image-Analysis/yeast_growth'

    deploy_root = '/deploy'

    project_root = os.path.join(deploy_root, project_name)

    data_path = os.path.join(project_root, 'data')
    code_path = os.path.join(project_root, 'code')
    output_path = os.path.join(project_root, 'output')
    working_path = os.path.join(project_root, 'working')

    mkdir_p(data_path)
    mkdir_p(output_path)
    mkdir_p(working_path)

    git_command = ('git', 'clone', project_url, code_path)

    subprocess.call(git_command)

    shutil.copy('/movingcastle/analyse.sh', project_root)

def analyse(args):
    print "Burning", args
    project_root = sys.argv[2]

    print project_root
    code_path = os.path.join(project_root, 'code')
    data_path = os.path.join(project_root, 'data')
    output_path = os.path.join(project_root, 'output')
    data_file = sys.argv[-1]
    inner_data_path = '/' + data_file


    command = ('docker',
               'run',
               '-v',
               '{}:/code'.format(code_path),
               '-v',
               '{}:/data'.format(data_path),
               '-v',
               '{}:/output'.format(output_path),
               'jicscicomp/jicbioimage',
               'python',
               '/code/scripts/yeast_growth.py',
               inner_data_path)

    subprocess.call(command)

    print ' '.join(command)   

def main():

    parser = argparse.ArgumentParser(description=__doc__)
 
    subparsers = parser.add_subparsers(help='sub-command help', 
                                        dest='subparser_name')

    parser_analyse = subparsers.add_parser('analyse', help='Run analysis')
    parser_analyse.add_argument('pwd', help='Working directory')
    parser_analyse.add_argument('data_file', help='Data filename')
    parser_analyse.set_defaults(func=analyse)

    parser_list = subparsers.add_parser('deploy', help='Initialise')
    parser_list.set_defaults(func=deploy)

    args = parser.parse_args()

    args.func(args)

    # db = DockerBroker()


    # myproj = Project('project.yml')

    # an = Analysis(myproj, "C0000230.ISQ")
    # an.stage_data()
    # an.debug_container()

    #print an.working


    #print db.list_images()
    #build_containers()
    #create_data_volumes()

if __name__ == "__main__":
    main()
