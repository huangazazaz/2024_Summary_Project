from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from DTO.RecordDTO import Record

Base = declarative_base()


class RecordMapper:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:hhelibeb@localhost:3306/summary')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, record: Record):
        try:
            self.session.add(record)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return 'fail'

    def get(self, id):
        record = self.session.query(Record).filter(Record.id == id).first()
        return record
