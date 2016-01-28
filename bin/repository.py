

__author__ = "Tyler Danstrom"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "0.1.5"
__maintainer__ = "Tyler Danstrom"
__email__ = "tdanstrom@uchicago.edu"
__status__ = "Development"

"""
This program is intended to transfer files from a designated staging area into a
designated repository area and change ownership of the files from whoever
processed the files to user:repository, group:repository

A corresponding script that calls all of the same library code but changee the
ownership to user:emabrgo,group:embargo will also be written.
"""

from argparse import ArgumentParser, Action
from os import _exit
from os.path import exists
from logging import DEBUG, ERROR, FileHandler, Formatter, getLogger, INFO, \
    StreamHandler
from sqlalchemy import Table

from ldrtransfer.batch import Batch
from ldrtransfer.database import Database

class ValidateDirectory(Action):
    def __call__(self, parser, args, value, option_string=None):
        if not exists(value):
            raise ValueError("The directory you entered does not exist.")
        setattr(args, self.dest, value)

def main():
    parser = ArgumentParser( \
                             description = "This is a tool for moving " + \
                             "accessions out of staging and into the archive.",
                             epilog = "Copyright University of Chicago" + \
                             " written by Tyler Danstrom " + \
"<tdanstrom@uchicago.edu>")

    parser.add_argument( \
                         "archive_directory",help="Enter the location of " + \
                         "the archive.",action=ValidateDirectory \
    )
    parser.add_argument( \
                         "source_root",help="Enter the root of the source " + \
                         "directory: that is the part of the path before " + \
                         "directory you want to accession",
                         action=ValidateDirectory \
    )
    parser.add_argument( \
                         "new_accession",
                         action = ValidateDirectory,
                         help = "Enter the directory that needs to be " + \
                         "accessioned." \
    )
    parser.add_argument( \
                         "-v", "--version", action="version", version="1.0.0" \
    )
    parser.add_argument( \
                         '-b','-verbose',help="set verbose logging",
                         action='store_const',dest='log_level',
                         const=INFO \
    )
    parser.add_argument( \
                         '-d','--debugging',help="set debugging logging",
                         action='store_const',dest='log_level',
                         const=DEBUG \
    )
    parser.add_argument( \
                         '-l','--log_loc',help="save logging to a file",
                         action="store_const",dest="log_loc",
                         const='./ldr_transfer.log' \
    )
    parser.add_argument( \
                         '-db', '--database_url', help = "Enter the  url" + \
                         " for the database", action = "store", default = \
                         "sqlite:////data/repository/databases/official/"+ \
                         "repositoryAccessions.db.new"
    )
    args = parser.parse_args()
    log_format = Formatter( \
                            "[%(levelname)s] %(asctime)s  " + \
                            "= %(message)s",
                            datefmt="%Y-%m-%dT%H:%M:%S" \
    )
    global logger
    logger = getLogger( \
                        "logger.repository.lib.uchicago" \
    )
    ch = StreamHandler()
    ch.setFormatter(log_format)
    if args.log_level:
        logger.setLevel(args.log_level)
    else:
        logger.setLevel(ERROR)
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    try:
        db = Database(args.database_url, ['record'])
        class Record(db.base):
            __table__ = Table('record',db.metadata,autoload=True)

        new_batch = Batch(args.new_accession, args.source_root)
        query = db.session.query(Record).filter(Record.receipt== \
                                                new_batch.accession)
        if query.count() != 1:
            logger.error("No such accession or too many accessions with " + \
                         "that identifier" \
            )
            return 1
        else:
            pass
        query = query.one()
        if query.publicAccessPermission == 0 \
           and query.publicDiscoveryPermission == 0:
            logger.error("You are using the wrong script. " + \
                         "Use the embargo script")
            return 1
        else:
            pass
        logger.debug(new_batch.accession)
        for i in new_batch.items:
            i.set_destination_path(args.archive_directory)
            i.copy_source_directory_tree_to_destination()
            i.move_into_new_location()
            i.set_destination_ownership("repository","repository")
            i.clean_out_source_directory_tree()
            logger.debug(i.destination)
        new_batch.clean_out_batch()
        db.close_session()
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
