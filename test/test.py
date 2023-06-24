import os
import requests
import redis
import random
import string
import json

# Step 1: Set a random API key to Redis with a low number of quota

# read the environment variables
redis_password = os.getenv('REDIS_PASSWORD')
redis_hostname = os.getenv('REDIS_HOSTNAME')

# Generate a random API key
api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Connect to Redis
r = redis.Redis(host=redis_hostname, password=redis_password)

# Set the API key in Redis with a low quota
quota = 5
r.hset("APIKEYS", api_key, quota)

# Step 2: Run a random number of calls equivalent to the example

# Prepare the request data
data = {
    "method": "getblock",
    "params":["000000000277ae93273121cb565ccc9b7b6458a7b5c60ff42bcdb291fada87b0"]
}

# Prepare the headers
headers = {
    "Content-Type": "application/json"
}

# Prepare the URL
url = f"http://openresty/{api_key}"

# Step 3: Check if the response is correct until the quota is depleted

for _ in range(quota):
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 200, "Expected HTTP 200 status code"

# Step 4: Make a last call and expect the response "Quota exceeded" and HTTP_TOO_MANY_REQUESTS

response = requests.post(url, headers=headers, data=json.dumps(data))
print(f"Final call status: {response.status_code}")
print(f"Final call body: {response.text}")

assert response.status_code == 429, "Expected HTTP 429 status code"
assert 'Quota exceeded' in response.text, "Expected 'Quota exceeded' in response"
