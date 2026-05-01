from flask import Blueprint, request, jsonify, abort
from .models import Movie, db

movies_bp = Blueprint('movies', __name__)

@movies_bp.route("/movies", methods=["GET", "POST", "DELETE"])
def movies_collection():
    if request.method == "GET":
        title_filter = request.args.get('title')
        if title_filter:
            movies = Movie.query.filter(Movie.title.ilike(f'%{title_filter}%')).all()
        else:
            movies = Movie.query.all()
        return jsonify([movie.to_dict() for movie in movies])

    elif request.method == "POST":
        data = request.get_json()
        if not data or not data.get('title'):
            abort(400, description="Title is required to create a movie.")

        new_movie = Movie(
            title=data['title'],
            description=data.get('description')
        )
        db.session.add(new_movie)
        db.session.commit()
        return jsonify(new_movie.to_dict()), 201

    elif request.method == "DELETE":
        db.session.query(Movie).delete()
        db.session.commit()
        return jsonify({'message': 'All movies deleted successfully'}), 200

@movies_bp.route("/movies/<int:movie_id>", methods=["GET", "PUT", "DELETE"])
def movie_resource(movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        abort(404, description=f"Movie with ID {movie_id} not found.")

    if request.method == "GET":
        return jsonify(movie.to_dict())

    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(400, description="Request body cannot be empty for PUT request.")

        if 'title' in data:
            movie.title = data['title']
        if 'description' in data:
            movie.description = data['description']
        
        db.session.commit()
        return jsonify(movie.to_dict())

    elif request.method == "DELETE":
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': f'Movie with ID {movie_id} deleted successfully'}), 204