FROM centos
MAINTAINER Matthew Hartley <Matthew.Hartley@jic.ac.uk>

RUN yum groupinstall -y 'Development Tools' && yum install -y\
    wget \
    libffi-devel \
    openssl-devel \
    python-devel

# Get and install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

RUN pip install gsutil redis

RUN yum clean all
