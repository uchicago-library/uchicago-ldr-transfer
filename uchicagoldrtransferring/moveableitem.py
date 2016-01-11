
from grp import getgrnam
from os import access, chown, listdir, mkdir, R_OK, rmdir, stat, walk
from os.path import abspath, dirname, exists, join, relpath
from pwd import getpwnam
from shutil import move
from uchicagoldr.item import Item

class MoveableItem(Item):
    destination = None
    root_path = None
    destination_root = None
    destination_permissions = 0o740

    def __init__(self, filepath, source_root, destination_root):
        assert exists(abspath(filepath))
        assert exists(abspath(destination_root))
        assert exists(abspath(source_root))
        self.root_path = source_root
        self.destination_root = destination_root
        self.filepath = filepath
        self.can_read = access(filepath, R_OK)
        self.set_sha256(self.find_sha256_hash())
        self.destination = self.calculate_destination_location()
    
    def calculate_destination_location(self):
        path_sans_root = relpath(self.filepath, self.root_path)
        destination_full_path = join(self.destination_root, path_sans_root)
        return destination_full_path
        
    def set_destination_path(self, destination_path):
        assert not exists(abspath(destination_path))
        self.destination = destination_path
     
    def copy_into_new_location(self):
        self.copy_source_directory_tree_to_destination()
        assert exists(dirname(self.destination))
        shutil.copyfile(self.filepath, self.destination)
        if exists(self.destination):
            new = Item(self.destination)
            self.destination_ownership(self.owner)
            self.destination(self.group)
            if new.find_sha256() == self.get_sha256():
                return namedtuple("result","status message") \
                    ("Good","")
            else:
                return namedtuple("result","status message") \
                    ("Bad","source checksum and destination checksum mismatch")
        else:
            return namedtuple("result","status message") \
                ("Bad","destination could not be created")

    def copy_source_directory_tree_to_destination(self):
        destination_directories = dirname(self.destination).split('/')
        directory_tree = ""
        for directory_part in destination_directories:
            directory_tree = join(directory_tree, directory_part)
            if not exists(directory_tree):
                mkdir(directory_tree, destination_permissions)
    
    def set_destination_ownership(self, user_name):
        uid = getpwnam(user_name).pw_uid
        gid = stat(self.destination).st_gid
        try:
            chown(self.destination, uid, gid)
            return (True,None)
        except Exception as e:
            return (False,e)

    def set_destination_group(self, group_name):
        uid = stat(self.destination).st_uid
        gid = getgrnam(group_name).gr_gid
        try:
            chown(self.destination, uid, gid)
            return (True,None)
        except Exception as e:
            return (False,e)
