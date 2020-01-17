import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For class to create table
Base = declarative_base()

# Defines table for SqlAlchemy
class Table(Base):
    __tablename__ = 'table'
    id = db.Column(db.String(), primary_key=True)
    ip = db.Column(db.String())
    ping_code = db.Column(db.Integer())
    ping_time = db.Column(db.Float())
    time_stamp = db.Column(db.String())
    description = db.Column(db.String())
    location = db.Column(db.String())
    group = db.Column(db.String())
    tv = db.Column(db.String())
    lastup = db.Column(db.String())
    lastlogon = db.Column(db.String())
    os = db.Column(db.String())
    version = db.Column(db.String())

# Define Database to connect to. Will create if empty
def connect_db(database):
    engine = db.create_engine(f'sqlite:///{database}')
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = db.MetaData()
    Base.metadata.create_all(engine)
    return engine, connection, session, metadata

def update_db(
    id,
    ip,
    ping_code,
    ping_time,
    time_stamp,
    description,
    location,
    group,
    tv,
    lastlogon,
    os,
    version,session):
    from modules.database import Table, Base
    data = [{'id': str(id),
             'ip': str(ip),
             'ping_code': int(ping_code),
             'ping_time': float(ping_time),
             'time_stamp': str(time_stamp),
             'description': str(description),
             'location': str(location),
             'group': str(group),
             'tv': str(tv),
             'lastlogon': str(lastlogon),
             'os': str(os),
             'version': str(version)}]
    if ping_code == 0:
        data[0]['lastup'] = str(time_stamp)
    existing_result = session.query(Table).filter_by(id=f'{id}').count()
    if existing_result > 0:
        session.bulk_update_mappings(Table, data)
        try:
            session.commit()
        except:
            session.rollback()
            return False
    else:
        session.bulk_insert_mappings(Table, data)
        try:
            session.commit()
        except:
            session.rollback()
            return False
    return True