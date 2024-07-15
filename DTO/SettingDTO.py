from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Setting(Base):
    __tablename__ = 'setting'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    style = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=False)
    cfg = Column(Integer, nullable=True)
    strength_model = Column(Float, nullable=True)
    strength_clip = Column(Float, nullable=True)
    denoise = Column(Float, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    batch_size = Column(Integer, nullable=False)

    def to_dict(self):
        return {'user_id': self.user_id, 'style': self.style, 'steps': self.steps, 'cfg': self.cfg,
                'strength_model': self.strength_model, 'strength_clip': self.strength_clip, 'denoise': self.denoise,
                'width': self.width, 'height': self.height, 'batch_size': self.batch_size, }

    def __str__(self):
        return (f"Setting(user_id={self.user_id}, style={self.style}, steps={self.steps}, cfg={self.cfg},"
                f"strength_model={self.strength_model},strength_clip={self.strength_clip}, denoise={self.denoise}, "
                f"width={self.width}, height={self.height}, batch_size={self.batch_size})")
