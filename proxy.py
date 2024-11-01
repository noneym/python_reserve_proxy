# proxy.py
docker
from flask import Flask, request, Response
import requests
import urllib3
import os

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Base URL of the target API, taken from environment variable
API_URL = os.getenv("API_URL")

# Proxy function
@app.route('/<path:url>', methods=['GET', 'POST'])
def proxy(url):
    # Full URL for the request
    full_url = f"{API_URL}/{url}"

    # Request headers taken directly from the incoming request
    headers = {key: value for key, value in request.headers if key.lower() not in ['host']}

    # Make the appropriate request
    if request.method == 'GET':
        print(f"GET request to {full_url} with headers: {headers}")
        resp = requests.get(full_url, headers=headers, params=request.args, verify=False)
    elif request.method == 'POST':
        print(f"POST request to {full_url} with headers: {headers} and data: {request.form}")
        resp = requests.post(full_url, headers=headers, data=request.form, verify=False)

    # Print response status and content
    print(f"Response status: {resp.status_code}")
    print(f"Response content: {resp.content}")

    # Prepare headers for the response, excluding problematic ones
    response_headers = {}
    for key, value in resp.headers.items():
        if key.lower() not in ['content-length', 'transfer-encoding', 'content-encoding']:
            response_headers[key] = value

    # Return the response
    return Response(resp.content, status=resp.status_code, headers=response_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
