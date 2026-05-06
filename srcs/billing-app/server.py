from flask import Flask
from app import create_app
from app.route import start_consoming


app=create_app()

if __name__ == "__main__":
    start_consoming(app)