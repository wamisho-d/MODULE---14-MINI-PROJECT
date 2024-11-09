# models.py - SQLAlchemy Models for Movie and Genre

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from config import engine

Base = declarative_base()

# Association table for many-to-many relationship
movie_genre_association = Table(
    'movie_genre', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    release_year = Column(Integer, nullable=False)
    genres = relationship("Genre", secondary=movie_genre_association, back_populates="movies")

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    movies = relationship("Movie", secondary=movie_genre_association, back_populates="genres")

# Create tables in the database
Base.metadata.create_all(bind=engine)
