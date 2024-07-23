from app import db
from datetime import datetime


class CompressedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    compressed_file_url = db.Column(db.String(255), nullable=False)