import redis
r = redis.Redis(host="host.docker.internal", port=6379, password="changeme", decode_responses=True) 

print(r.ping())
print(r.set(name="야", value("호"))
print(r.get(name="야")
