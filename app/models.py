# app/models.py

from . import db

# states

# Define SQLAlchemy models to represent database tables

'''example code on how to use models in flask'''

# class Film(db.Model):
#     __tablename__ = "film"
#     film_id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     description = db.Column(db.Text)
#     release_year = db.Column(db.Integer)
#     rating = db.Column(db.String(10))
#     special_features = db.Column(db.String(255))
#     # Define the relationship with film_actor
#     actors = db.relationship("FilmActor", back_populates="film")
#
#
# class Actor(db.Model):
#     __tablename__ = "actor"
#
#     actor_id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(45), nullable=False)
#     last_name = db.Column(db.String(45), nullable=False)
#     # Define the relationship with film_actor
#     films = db.relationship("FilmActor", back_populates="actor")
