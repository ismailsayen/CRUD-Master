import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from the shared .env file at the project root
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '../../.env')
load_dotenv(dotenv_path)

# Get the INVENTORY_PORT from the .env file, default to 8080 if not set
PORT = os.environ.get('INVENTORY_PORT', 8081)
BASE_URL = f"http://localhost:{PORT}/api/movies"

def print_response(response, message=""):
    """Helper function to print API responses."""
    print(f"\n--- {message} ---")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        print("Response Text:")
        print(response.text)
    print("-" * 30)

def test_api():
    print("Starting API tests for Inventory App...")

    # 1. Delete all existing movies (cleanup before test)
    print("Attempting to delete all movies for a clean slate...")
    response = requests.delete(BASE_URL)
    print_response(response, "DELETE All Movies")

    # 2. Create a new movie
    new_movie_data = {"title": "The Matrix", "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."}
    response = requests.post(BASE_URL, json=new_movie_data)
    print_response(response, "POST New Movie (The Matrix)")
    matrix_id = response.json().get('id')

    # 3. Create another movie
    new_movie_data_2 = {"title": "Inception", "description": "A thief who steals information by entering people's dreams is given the inverse task of planting an idea into a target's subconscious."}
    response = requests.post(BASE_URL, json=new_movie_data_2)
    print_response(response, "POST New Movie (Inception)")
    inception_id = response.json().get('id')

    # 4. Get all movies
    response = requests.get(BASE_URL)
    print_response(response, "GET All Movies")

    # 5. Get a specific movie by ID (The Matrix)
    if matrix_id:
        response = requests.get(f"{BASE_URL}/{matrix_id}")
        print_response(response, f"GET Movie by ID: {matrix_id} (The Matrix)")
    else:
        print("\nSkipping GET by ID for The Matrix as ID was not retrieved.")

    # 6. Get movies by title filter
    response = requests.get(f"{BASE_URL}?title=Matrix")
    print_response(response, "GET Movies by Title Filter 'Matrix'")

    # 7. Update a movie (Inception)
    if inception_id:
        updated_movie_data = {"title": "Inception (Director's Cut)", "description": "A thief who steals information by entering people's dreams is given the inverse task of planting an idea into a target's subconscious. Extended version."}
        response = requests.put(f"{BASE_URL}/{inception_id}", json=updated_movie_data)
        print_response(response, f"PUT Update Movie by ID: {inception_id} (Inception)")
    else:
        print("\nSkipping PUT by ID for Inception as ID was not retrieved.")

    # 8. Get the updated movie to verify
    if inception_id:
        response = requests.get(f"{BASE_URL}/{inception_id}")
        print_response(response, f"GET Updated Movie by ID: {inception_id} (Inception)")

    # 9. Delete a specific movie by ID (The Matrix)
    if matrix_id:
        response = requests.delete(f"{BASE_URL}/{matrix_id}")
        print_response(response, f"DELETE Movie by ID: {matrix_id} (The Matrix)")

    # 10. Get all movies again to confirm deletion
    response = requests.get(BASE_URL)
    print_response(response, "GET All Movies (after deleting The Matrix)")

    print("API tests completed.")

if __name__ == "__main__":
    test_api()