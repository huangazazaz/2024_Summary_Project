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

    def update_setting(self, update_fields):
        setting = self.session.query(Setting).filter_by(username=update_fields['username']).first()

        # 如果找到记录，更新字段
        if setting:
            for field, value in update_fields.items():
                setattr(setting, field, value)
            # 提交事务
        else:
            self.session.add(update_fields)
        self.session.commit()
        return 'success'

    def add_setting(self, setting):
        try:
            setting = self.session.query(Setting).filter_by(username=update_fields['username']).first()
            if setting is None:
                self.session.add(setting)
                self.session.commit()
                return 'success'
            else:
                return 'existed'
        except Exception as e:
            self.session.rollback()
            return 'fail'

    def get_setting(self, username):
        setting = self.session.query(Setting).filter_by(username=username).first()
        if setting:
            return setting
        else:
            return Setting(username=username, style=0, steps=30, cfg=4, strength_model=0.7, strength_clip=0.7,
                           denoise=1, width=1024, height=576, batch_size=1)
