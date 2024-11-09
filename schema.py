# schema.py - GraphQL Schema with Mutations and Queries
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Movie, Genre
from config import SessionLocal

# Initialize the session
db_session = SessionLocal()

# GraphQL Types
class MovieType(SQLAlchemyObjectType):
    class Meta:
        model = Movie

class GenreType(SQLAlchemyObjectType):
    class Meta:
        model = Genre

# Input type for Mutations
class GenreInput(graphene.InputObjectType):
    name = graphene.String(required=True)

# Genre Mutations
class CreateGenre(graphene.Mutation):
    class Arguments:
        input = GenreInput(required=True)

    genre = graphene.Field(lambda: GenreType)

    def mutate(self, info, input):
        name = input.name
        if not name or len(name) > 50:
            raise Exception("Genre name is required and must not exceed 50 characters.")
        
        genre = Genre(name=name)
        db_session.add(genre)
        db_session.commit()
        return CreateGenre(genre=genre)

class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(lambda: GenreType)

    def mutate(self, info, id, name):
        genre = db_session.query(Genre).get(id)
        if not genre:
            raise Exception("Genre not found.")
        if not name or len(name) > 50:
            raise Exception("Genre name must not exceed 50 characters.")

        genre.name = name
        db_session.commit()
        return UpdateGenre(genre=genre)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        genre = db_session.query(Genre).get(id)
        if not genre:
            raise Exception("Genre not found.")

        db_session.delete(genre)
        db_session.commit()
        return DeleteGenre(success=True)

# Queries for Movie-Genre Relationships
class Query(graphene.ObjectType):
    get_movies_by_genre = graphene.List(MovieType, genre_id=graphene.Int(required=True))
    get_genres_by_movie = graphene.List(GenreType, movie_id=graphene.Int(required=True))

    def resolve_get_movies_by_genre(self, info, genre_id):
        genre = db_session.query(Genre).get(genre_id)
        if not genre:
            raise Exception("Genre not found.")
        return genre.movies

    def resolve_get_genres_by_movie(self, info, movie_id):
        movie = db_session.query(Movie).get(movie_id)
        if not movie:
            raise Exception("Movie not found.")
        return movie.genres

# Mutation root
class Mutation(graphene.ObjectType):
    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()

# Final Schema
schema = graphene.Schema(query=Query, mutation=Mutation)