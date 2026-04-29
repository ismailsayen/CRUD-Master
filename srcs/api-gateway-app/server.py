from flask import Flask,request

app = Flask(__name__)


@app.route("/<path:path>")
def hello_world(path):
    BILLING="http://127.0.0.1:8082"
    INVENTORY="http://127.0.0.1:8080"
    print("==>",path)
    return "<p>Hello, api-Getway!</p>"

if __name__ == "__main__":
    app.run()