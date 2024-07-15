from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    url = Column(String, nullable=False)
    style = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=True)
    cfg = Column(Integer, nullable=True)
    strength_model = Column(Float, nullable=True)
    strength_clip = Column(Float, nullable=True)
    denoise = Column(Float, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    batch_size = Column(Integer, nullable=True)
    generation_time = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'url': self.url,
            'style': self.style,
            'steps': self.steps,
            'cfg': self.cfg,
            'strength_model': self.strength_model,
            'strength_clip': self.strength_clip,
            'denoise': self.denoise,
            'width': self.width,
            'height': self.height,
            'batch_size': self.batch_size,
            'generation_time': self.generation_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __str__(self):
        return (f"User(id={self.id}, user_id={self.user_id}, text='{self.text}', "
                f"url='{self.url}', style={self.style}, steps={self.steps}, "
                f"cfg={self.cfg}, strength_model={self.strength_model}, "
                f"strength_clip={self.strength_clip}, denoise={self.denoise}, "
                f"width={self.width}, height={self.height}, batch_size={self.batch_size}, "
                f"generation_time='{self.generation_time}')")
