from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from DTO.UserDTO import User  # 确保 UserDTO 中定义了 User 类，且该类继承自 Base

Base = declarative_base()


class UserMapper:
    def __init__(self):
        # 请根据实际数据库驱动和凭证修改下面的连接字符串
        self.engine = create_engine('mysql+pymysql://root:hhelibeb@localhost:3306/summary')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def register(self, user: User):
        try:
            self.session.add(user)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return 'fail'

    def get(self, username):
        user = self.session.query(User).filter(User.username == username).first()
        print(user)
        return user
