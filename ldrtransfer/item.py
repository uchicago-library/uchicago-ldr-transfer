from hashlib import md5, sha256
from os import access, chown, listdir, mkdir, rmdir, stat, R_OK, walk
from os.path import dirname, exists, join, relpath
from mimetypes import guess_type, read_mime_types
from shutil import move

class Item(object):
    root_path = ""
    filepath = ""
    destination = ""
    sha256_hash = ""
    md5_hash = ""
    accession = ""
    mimetype = ""
    can_read = False
    has_technical_md = False
    
    def __init__(self, path, root):
        if access(path, R_OK):
            self.can_read = True
        else:
            pass
        self.root_path = root
        self.filepath = path
        self.find_file_accession()
        self.get_file_mime_type()
        self.get_file_size()
        self.sha256_hash = self.get_file_hash(sha256)
        self.md5_hash = self.get_file_hash(md5)
        self.find_technical_metadata()
        
    def get_file_hash(self, hash_type, blocksize=65536):
        blocksize = 65536
        hash = hash_type()
        afile = open(self.filepath,'rb')
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hash.update(buf)
            buf = afile.read(blocksize)
        return hash.hexdigest()

    def find_file_accession(self):
        relative_path = relpath(self.filepath, self.root_path)
        accession, *tail = relative_path.split('/')
        self.accession = accession
        
    def get_file_size(self):
        self.file_size = stat(self.filepath).st_size        
        return True
        
    def get_file_mime_type(self):
        self.mimetype = guess_type(self.filepath)[0]
        return True
    
    def find_technical_metadata(self):
        fits_filepath = join(self.filepath,'.fits.xml')
        if exists(fits_filepath):
            self.has_technical_md = True
        else:
            pass
        return True

    def set_destination_path(self, new_root_directory):
        path_sans_root = relpath(self.filepath, self.root_path)
        destination_full_path = join(new_root_directory, path_sans_root)
        self.destination = destination_full_path
        return True
    
    def move_into_new_location(self):
        try:
            move(self.filepath, self.destination)
            return (True,None)
        except Exception as e:
            error = e
            return (False,e)
        
    def copy_source_directory_tree_to_destination(self):
        destination_directories = dirname(self.destination).split('/')
        directory_tree = ""
        for f in destination_directories:
            directory_tree = join(directory_tree,f)
            if not exists(directory_tree):
                try:
                    mkdir(directory_tree,0o740)
                except Exception as e:
                    return (False,e)
        return (True,None)
    
    def clean_out_source_directory_tree(self):
        directory_tree = dirname(self.filepath)
        for src_dir, dirs, files in walk(directory_tree):
            try:
                rmdir(src_dir)
                return (True,None)
            except Exception as e:
                return (False,e)
    
    def set_destination_ownership(self, user_name, group_name):
        uid = getpwnam(user_name).pw_uid
        gid = getgrnam(group_name).gr_gid
        try:
            chown(self.destination, uid, gid)
            return (True,None)
        except Exception as e:
            return (False,e)
    
