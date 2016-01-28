
from os import access, listdir, rmdir, R_OK
from os.path import join, isfile, isdir, relpath

from ldrtransfer.item import Item

class Batch(object):
    items = []
    directory = ""
    
    def __init__(self, batch_directory, root_of_batch):
        self.directory = batch_directory
        directory_relative_to_root = relpath(self.directory, root_of_batch)
        accession, *tail = directory_relative_to_root.split('/')
        self.accession = accession
        self.items = self.find_all_files(self.directory, root_of_batch)
            
    def find_all_files(self, directory, directory_root):
        flat_list = listdir(directory)
        for file_basename in flat_list:
            fullpath = join(directory, file_basename)
            if isfile(fullpath):
                i = Item(fullpath, directory_root)
                yield i
            elif isdir(fullpath):
                for n in self.find_all_files(fullpath, directory_root):
                    yield n

    def clean_out_batch(self):
        rmdir(self.directory)
