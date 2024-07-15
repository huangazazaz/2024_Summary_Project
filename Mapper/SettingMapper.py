from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from DTO.SettingDTO import Setting

Base = declarative_base()


class SettingMapper:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:hhelibeb@localhost:3306/summary')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, setting: Setting):
        try:
            self.session.add(setting)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return 'fail'

    def get(self, user_id):
        setting = self.session.query(Setting).filter(Setting.user_id == user_id).first()
        print(setting)
        return setting
