from os import access, listdir, rmdir, R_OK
from os.path import join, isfile, isdir, relpath
from uchicagoldr.batch import Directory
from uchicagoldrtransferring.moveableitem import MoveableItem
from uchicagoldrconfig.LDRConfiguration import LDRConfiguration

config = LDRConfiguration('/media/sf_source_code/ldr_configuration/config/').get_config()

        
class MoveableDirectory(Directory):
    def __init__(self, directory_path, source_root, destination_root, 
                 items=None):
        self.directory_path = directory_path

    def add_item(self, i):
        assert isinstance(i, Item)
        self.items.add(i)

class StagingDirectory(MoveableDirectory):
    def __init__(self, directory_path, source_root, destination_root, 
                 ead_identifier, accession_number, embargo=False, items=None):
        assert exists(directory_path)
        assert re_compile('^\d{4}[-]\d{3}$').match(accession_number)
        assert re_compile('^ICU.(.*)$').match(ead_identifier)
        self.ead_identifier = ead_identifier
        self.accession_number = accession_number
        self.accession_noid = self.mint_accession_identifier()
        if embargo:
            self.user = "embargo"
            self.group = "embargo"
        else:
            self.user = "repository"
            self.group = "repository"
        self.directory_path = directory_path
        self.items = self.walk_directory_picking_files(directory_path)

    def mint_accession_identifier(self):
        url_data = config['accessionminter']['url']
        if url_data.status == 200:
            url_data = url_data.read()
        else:
            raise ValueError("Could not fetch batch identifier from " +
                             "RESTful NOID minter")
        return url_data.split('61001/').rstrip()

    def ingest():
        for n in self.items:
            i.copy_into_new_location()


class FileWalker(object):
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.files = self.walk_directory_picking_files()

    def __iter__(self):
        return self.files

    def walk_directory_picking_files(self):
        flat_list = listdir(self.directory_path)
        while flat_list:
            node = flat_list.pop()
            fullpath = join(self.directory_path, node)
            if isfile(fullpath):
                yield fullpath
            elif isdir(fullpath):
                for child in listdir(fullpath):
                    flat_list.append(join(fullpath, child))

if __name__ == "__main__":
    f = FileWalker('/media/sf_source_code/uchicagoldr-transfer/source_root')
    for i in f:
        mi = MoveableItem(i,'/media/sf_source_code/uchicagoldr-transfer/source_root',
                          '/media/sf_source_code/uchicagoldr-transfer/destination')
        print((mi.filepath, mi.destination))
# class Batch(object):
#     items = []
#     directory = ""
    
#     def __init__(self, batch_directory, root_of_batch):
#         self.directory = batch_directory
#         directory_relative_to_root = relpath(self.directory, root_of_batch)
#         accession, *tail = directory_relative_to_root.split('/')
#         self.accession = accession
#         self.items = self.find_all_files(self.directory, root_of_batch)
            
#     def find_all_files(self, directory, directory_root):
#         flat_list = listdir(directory)
#         for file_basename in flat_list:
#             fullpath = join(directory, file_basename)
#             if isfile(fullpath):
#                 i = Item(fullpath, directory_root)
#                 yield i
#             elif isdir(fullpath):
#                 for n in self.find_all_files(fullpath, directory_root):
#                     yield n

#     def clean_out_batch(self):
#         rmdir(self.directory)
