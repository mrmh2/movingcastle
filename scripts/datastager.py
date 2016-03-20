"""Data stager."""

import os
import shutil

class DataStager(object):

    def __init__(self, source, destination):
        # TODO - something URI like to handle something that isn't just copy
        self.source = source
        self.destination = destination

    def stage_file(self, filename):

        full_source_path = os.path.join(self.source, filename)
        full_dest_path = os.path.join(self.destination, filename)

        shutil.copyfile(full_source_path, full_dest_path)