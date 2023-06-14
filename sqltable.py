'''Python file for the sql table containing the gateway data'''
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

class SQLTable():
    '''Class to create the SQLTable'''

    def __init__(self):
        '''Method to init the SQLTable Class'''

        self.engine = db.create_engine('sqlite:///users.db', echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata_obj = db.MetaData()
        self.gateway = db.Table(
            'Gateway',
            self.metadata_obj,
            db.Column('gateway_id', db.String),
            db.Column('last_status_received_at', db.String),
            db.Column('ip', db.String),
        )
        self.metadata_obj.create_all(self.engine)


    def checkIfInserted(self, gateway_id):
        #select('*').select_from(self.gateway).where(self.gateway.c.gateway_id == gateway_id)
        return self.session.query(self.gateway).filter(self.gateway.c.gateway_id == gateway_id).first()
