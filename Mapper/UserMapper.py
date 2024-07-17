from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from DTO.UserDTO import User

Base = declarative_base()


class UserMapper:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:hhelibeb@localhost:3306/summary')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def register(self, user: User):
        try:
            user = self.session.query(User).filter(User.username == user.username).first()
            if user:
                return 'user existed'
            self.session.add(user)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return 'server error'

    def login(self, username, password):
        user = self.session.query(User).filter(User.username == username).first()

        if not user:
            return 'user not exist'

        if not password == user.password:
            return 'password error'

        return 'success'
