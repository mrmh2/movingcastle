"""Docker-py backend."""

import os

import docker
from docker.client import Client

def docker_client_from_env():

    environ = os.environ

    tcp_host = environ['DOCKER_HOST']
    docker_host = 'https' + tcp_host[3:]

    cert_base = environ['DOCKER_CERT_PATH']

    cert_path = os.path.join(cert_base, 'cert.pem')
    key_path = os.path.join(cert_base, 'key.pem')

    client_cert = (cert_path, key_path)

    tls_config = docker.tls.TLSConfig(client_cert)

    client = Client(base_url=docker_host, tls=tls_config)

    return client

class DockerBroker(object):

    def __init__(self):
        self.client = docker_client_from_env()

    def list_images(self):

        return self.client.images()