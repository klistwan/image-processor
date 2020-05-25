from dataclasses import dataclass
import datetime

from app import db

@dataclass
class Thumbnail(db.Model):
    __tablename__ = "thumbnails"

    id: str
    original_url: str
    resized_url: str
    status: str

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.Date, onupdate=datetime.datetime.now)
    original_url = db.Column(db.String(100), nullable=False)
    resized_url = db.Column(db.String(100))
    status = db.Column(db.Enum('queued','completed','failed'), nullable=False, default='queued')

    def __init__(self, uuid, original_url):
        self.id = uuid
        self.original_url = original_url

    def __repr__(self):
        return f"<Thumbnail: {self.id}, {self.original_url}"
