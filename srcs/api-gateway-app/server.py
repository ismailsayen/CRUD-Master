from flask import Flask
from app import forward_to_inventory as inventory
app = Flask(__name__)

def Proxy(url:str):
    return inventory.forward_to_inventory(url)
    
@app.route("/<path:path>")
def server(path:str, methods=["GET", "POST", "PUT", "DELETE"]):
    BILLING="http://127.0.0.1:8082"
    INVENTORY="http://127.0.0.1:8080"
    if path.startswith("api/movies"):
        url=f"{INVENTORY}/{path}"
        return Proxy(url)
    elif path.startswith("api/billing"):
        url=f"{BILLING}/{path}"
    else:
        return "SERVICE NOT FOUND", 404
    
    

if __name__ == "__main__":
    app.run(port=8081)