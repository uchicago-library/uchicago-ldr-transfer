
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,MetaData,Table

class Database(object):
    session = None
    base = None
    metadata = None

    class Record():
        def __init__(self,table_name, metadata):
            __table__ = Table(table_name, metadata, autoload=True)
     
    
    def __init__(self, database_url, tables_to_bind):
        engine = create_engine(database_url)
        session = sessionmaker(bind=engine)
        session = session()
        metadata = MetaData()
        self.base = declarative_base()
        metadata.reflect( \
                          bind=engine,only=tables_to_bind \
        )
        engine.connect()
        self.metadata = metadata

        self.session = session

    def close_session(self):
        self.session.close()
