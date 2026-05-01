from flask import request,Response
import requests

def forward_to_inventory(url:str):
    
    headers = {}
    for key, value in request.headers:
        if key != "Host":
            headers[key] = value        
    resp=requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.data,
        cookies=request.cookies,
        allow_redirects=False
    )
    response = Response(resp.content, resp.status_code)
    for key, value in resp.headers.items():
        response.headers[key] = value

    return response
