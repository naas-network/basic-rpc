# basic-rpc

# TLDR Diagram

https://mermaid.live/edit#pako:eNplkMFuwjAMhl8l8imT2heoJibaMMFhMAHaYcrFagyNaJPKTTdNlHefYWOXKQfHvz_9lv8z1NERFHBk7Bu1NzZc31xv45iIH2wodbmv1FooaSpdNejDMsaTdEZv2PmA7aDmr6s7s9Bbqkce_AepJbU9sdrFQ_pEvk7FO8_zWXmrs-nZt7KG3NNU_VPMr_LmUR0p_bmuwlCz75OPYVrIvkeBhDVSxAQy6Ig79E6uOtuglIXUUEcWCvk65JMFGy7C4Zji7ivUUCQeKYOxd5jIeJQwurtIzqfILz8p3cLKoMfwHqMgB7mdLt8pWG6m


# Architecture
## nginx.conf

Here's a high-level description of what this code is doing:

1. The access_by_lua_block directive is used to run Lua code for each request. This code is run before Nginx processes the request.
2. The Lua code connects to Redis and authenticates using the password obtained from the environment variable REDIS_PASSWORD.
3. It extracts the API key from the URI and the method from the request body.
4. The method is checked against an array of allowed methods. If the method is not allowed or not present, a HTTP 403 Forbidden status is returned.
5. If the method is allowed, it attempts to fetch the response from Redis cache. If a valid cache entry is found, it returns the cached response.
6. If a valid cache entry is not found, it sets the authorization header for Bitcoin Core and proxies the request to Bitcoin Core.
7. If the Bitcoin Core responds with a HTTP 200 OK status, it caches the response in Redis and increments the quota counter for the API key.