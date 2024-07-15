from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from DTO.SettingDTO import Setting  # 确保 UserDTO 中定义了 User 类，且该类继承自 Base

Base = declarative_base()


class SettingMapper:
    def __init__(self):
        # 请根据实际数据库驱动和凭证修改下面的连接字符串
        self.engine = create_engine('mysql+pymysql://root:hhelibeb@localhost:3306/summary')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, setting: Setting):
        self.session.add(setting)
        self.session.commit()

    def get(self, user_id):
        setting = self.session.query(Setting).filter(Setting.user_id == user_id).first()
        print(setting)
        return setting
