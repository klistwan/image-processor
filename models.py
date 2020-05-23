from app import db


class Thumbnail(db.Model):
    __tablename__ = "thumbnails"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.Date)
    original_url = db.Column(db.String(100), nullable=False)
    resized_url = db.Column(db.String(100))
    status = db.Column(db.Enum('queued','completed','failed'), nullable=False, server_default='queued')

    def __init__(self, original_url):
        self.original_url = original_url

    def __repr__(self):
        return f"<Thumbnail: {self.id}, {self.original_url}"