from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    register_time = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'register_time': self.register_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __str__(self):
        return (f"User(username={self.username}, email={self.email}, "
                f"avatar={self.avatar}, registered at {self.register_time.strftime('%Y-%m-%d %H:%M:%S')})")
