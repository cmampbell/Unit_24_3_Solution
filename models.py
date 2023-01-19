"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

default_image = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    '''Cupcake SQLAlchemy model'''

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float)
    image = db.Column(db.String, nullable=False, default=default_image)

    def serialize(self):
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }

    def update(self, json):
        self.flavor = json.get('flavor', self.flavor)
        self.size = json.get('size', self.size)
        self.rating = json.get('rating', self.rating)
        self.image = json.get('image', self.image)