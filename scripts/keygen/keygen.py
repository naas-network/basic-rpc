import os
import redis
import hashlib
import csv
import uuid
from flask import Flask, jsonify

# read the environment variables
redis_password = os.getenv('REDIS_PASSWORD')
redis_hostname = os.getenv('REDIS_HOSTNAME')

# create a connection to Redis
r = redis.Redis(host=redis_hostname, password=redis_password)

# initialize Flask
app = Flask(__name__)

@app.route('/keys', methods=['GET'])
def get_keys():
    # fetch the first 100 keys and their quotas from Redis
    keys = r.hgetall('APIKEYS')
    keys = {k.decode('utf-8'): int(v) for k, v in keys.items()}  # decode keys and values from bytes to string/int
    keys = dict(list(keys.items())[:100])  # get the first 100 keys

    return jsonify(keys), 200

# create the API keys only if they do not exist
if not r.exists('APIKEYS'):

    # create a csv file
    with open('naas-apikeys/api_keys.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Api key", "Credit", "Assigned to Manager", "Username"])

        # generate 1000 API keys
        for _ in range(1000):
            # generate a unique API key
            api_key = hashlib.sha256(uuid.uuid4().bytes).hexdigest()

            # set the API key in Redis with a quota of 10000
            r.hset('APIKEYS', api_key, 10000)

            # write the API key to the csv file
            writer.writerow([api_key, 10000, '', ''])
    # print that the init is done
    print('API keys generated')
else:
    print('API keys already exist')

# start the Flask server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
