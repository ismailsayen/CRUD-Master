from flask import Flask

app = Flask(__name__)

@app.route("/api/movies")
def hello_world():
    return "<p>Hello, Inventory!</p>"

if __name__ == "__main__":
    app.run()