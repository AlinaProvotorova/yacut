from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), unique=True, nullable=False)
    short = db.Column(db.String(128), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            url=self.original,
            short_link='http://localhost/' + self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data: dict):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])


