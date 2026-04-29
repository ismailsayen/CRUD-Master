from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, api-Getway!</p>"

if __name__ == "__main__":
    app.run()