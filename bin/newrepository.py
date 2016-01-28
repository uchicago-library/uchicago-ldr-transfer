from argparse import Action, ArgumentParser
from collections import namedtuple
from hashlib import md5
from logging import DEBUG, ERROR, FileHandler, Formatter, getLogger, INFO, \
    StreamHandler
from mimetypes import MimeTypes
from os import _exit, stat, walk
from os.path import exists, join
from uchicagoldrtransferring.moveablebatch import FileWalker, MoveableItems
from uchicagoldrtransferring.moveableitem import MoveableItem
from uchicagoldrastorage.models import engine, Record
from sqlalchemy.orm.session import sessionmaker

def main(directory):
    f = FileWalker(directory)
    mitems = MoveableItems()
    for i in f:
        mi = MoveableItem(i, source_root, destination_root)
        mitems.add_item(mi)
    return mitems

if __name__ == "__main__":
    _exit(main())
    
# if __name__ == "__main__":
#     f = FileWalker('/media/sf_source_code/uchicagoldr-transfer/source_root')
#     #ai = AccessionIdentifier()

#     mitems = MoveableItems()
#     for i in f:
#         mi = MoveableItem(i,'/media/sf_source_code/uchicagoldr-transfer/source_root',
#                           '/media/sf_source_code/uchicagoldr-transfer/destination')
#         mitems.add_item(mi)
#     print(mitems.items)



# class ValidateDirectory(Action):
#     def __call__(self, parser, args, value, option_string=None):
#         setattr(args, self.dest, value)

# class ValidateAccession(Action):
#     def gethash(self, afile, blocksize=65536):
#         hash = md5()
#         buf = afile.read(blocksize)
#         while len(buf) > 0:
#             hash.update(buf)
#             buf = afile.read(blocksize)
#         return hash.hexdigest()
    
#     def __init__(self, option_strings, dest, nargs=None, **kwargs):
#         if nargs is not None:
#             raise ValueError("nargs not allowed")
#         super(ValidateAccession, self).__init__(option_strings, dest, **kwargs)

#     def __call__(self, parser, args, value, option_string=None):
#         staging_directory = args.source_root
#         directory_path = join(staging_directory,value)
#         technical_metadata = []
#         regular_files = []
#         total_files = 0
#         total_technical_files = 0
#         mimes = MimeTypes()

#         if exists(directory_path):
#             pass
#         else:
#             raise ValueError("the accession you entered does not exist "+
#                              "in the staging directory.")
#         for root,directory,files in walk(directory_path):
#             fd = namedtuple("file_data","filepath size mimetype checksum")
#             technical_metadata.extend([fd(join(root,item),
#                                           stat(join(root,item)).st_size,
#                                           mimes.guess_type(join(root,item),'rb'),
#                                           self.gethash(open(join(root,item),'rb'))) \
#                                        for item in files if item.endswith('fits.xml')])
#             regular_files.extend([fd(join(root,item),
#                                      stat(join(root,item)).st_size,
#                                      mimes.guess_type(join(root,item),'rb'),                                     
#                                      self.gethash(open(join(root,item),'rb'))) \
#                                   for item in files if not(item.endswith('fits.xml'))])

#             total_files += len(files)

#         if (len(technical_metadata) != len(regular_files)) \
#            or ([f for f in regular_files if f.size <= 0] \
#                or [f for f in technical_metadata if f.size <= 0]):
#             t = [f.filepath.split('.fits.xml')[0] for f in technical_metadata]
#             t2 = [f[0] for f in \
#                  [(f,True) if f.filepath in t else (f,False) for f in regular_files] 
#                  if f[1] == False]
#             t3 = [f[0] for f in \
#                   [(f,True) if f.size > 0 else (f,False) for f in regular_files]
#                   if f[1] == False]
#             t4 = [f[0] for f in \
#                   [(f,True) if f.size > 0 else (f,False) for f in technical_metadata]
#                   if f[1] == False]
#             t3.extend(t4)
#             if len(t2) > 0:
#                 t2_string_list = '\n'.join([f.filepath for f in t2])
#             else:
#                 t2_string_list = None
#             if len(t3) > 0:
#                 t3_string_list = '\n'.join([f.filepath for f in t3])
#             else:
#                 t3_string_list = None
#             first_list_msg = "\nThe following files do not have techical metadata: \n\n" + \
#                              t2_string_list if t2_string_list else ""
#             second_list_msg = "\nThe following files are empty: \n\n" + \
#                               t3_string_list if t3_string_list else ""
#             raise ValueError("The following errors occured for %s" % value +
#                              first_list_msg + "\n" +
#                              second_list_msg + "\n")
#         else:
#             setattr(args, self.dest, regular_files+technical_metadata)

# def main():
#     try:
#         parser = ArgumentParser( \
#                                  description = "This is a tool for moving " + \
#                                  "accessions out of staging and into the archive.",
#                                  epilog = "Copyright University of Chicago" + \
#                                  " written by Tyler Danstrom" + \
#                                  "<tdanstrom@uchicago.edu>" \
#                              )
#         parser.add_argument( \
#                              "archive_directory",help="Enter the location of " + \
#                              "the archive.",action=ValidateDirectory \
#                          )
#         parser.add_argument( \
#                              "source_root",help="Enter the root of the source " + \
#                              "directory: that is the part of the path before " + \
#                              "directory you want to accession",
#                              action=ValidateDirectory \
#                          )
#         parser.add_argument( \
#                              "new_accession",
#                              action = ValidateAccession,
#                              help = "Enter the directory that needs to be " + \
#                              "accessioned." \
#                          )
#         parser.add_argument( \
#                              "-v", "--version", action="version", version="1.0.0" \
#                          )
#         parser.add_argument( \
#                              '-b','-verbose',help="set verbose logging",
#                              action='store_const',dest='log_level',
#                              const=INFO \
#                          )
#         parser.add_argument( \
#                              '-d','--debugging',help="set debugging logging",
#                              action='store_const',dest='log_level',
#                              const=DEBUG \
#                          )
#         parser.add_argument( \
#                              '-l','--log_loc',help="save logging to a file",
#                              action="store_const",dest="log_loc",
#                              const='./ldr_transfer.log' \
#                          )

#         args = parser.parse_args()
#         new_batch = Batch(args.new_accession, args.source_root)

#         for i in new_batch.items:
#             # first build the new destination of the file 
#             i.set_destination_path(args.archive_directory)
#             # # second copy the source tree sans files from old locaiton to new
#             i.copy_source_directory_tree_to_destination()
#             # # third move the actual file into the new location
#             i.move_into_new_location()
#             # # fourth set the new ownership and group membership of the file
#             i.set_destination_ownership("repository","repository")
#             # # fifth empty out the old location by trying to delete the
#             # # directory: this will fail if the directory still has file(s)
#             # # in it
#             i.clean_out_source_directory_tree()
#             # logger.debug(i.destination)
#         return 0
#     except KeyboardInterrupt:
#         return 131

# if __name__ == "__main__":
#     _exit(main())
