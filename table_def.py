import datetime
import json

from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
 
engine = create_engine('sqlite:///image_processor.db', echo=True)
Base = declarative_base()
 

class Thumbnail(Base):
    __tablename__ = "thumbnails"

    id = Column(Integer, primary_key=True)
    created_at = Column(Date, default=datetime.datetime.utcnow)
    updated_at = Column(Date, onupdate=datetime.datetime.now)
    original_url = Column(String(100), nullable=False)
    resized_url = Column(String(100), nullable=True)
    status = Column(Enum('queued','completed','failed'), default='queued')

    def __init__(self, original_url):
        self.original_url = original_url

    def __repr__(self):
        return f"<Thumbnail: {self.id}, {self.original_url}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


Base.metadata.create_all(engine)