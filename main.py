import redis
from threading import Thread
from ratelimiter import RateLimiter

client = redis.Redis(host="redis-server")

# limiter para medida de TPS usando Redis
def limiter(key, limit):
    req = client.incr(key)
    if req == 1:
        client.expire(key, 1)
        ttl = 1
    else:
        ttl = client.ttl(key)
    if req > limit:
        return {
            "call": False,
            "ttl": ttl
        }
    else:
        return {
            "call": True,
            "ttl": ttl
        }

# callback rate limiter interno 
def limited(until):
    print("Rate Limited")

# função que utiliza rate limit interno
def test_interno():
    return "Hello Word"

# função a ser limitada
def test():
    res = limiter("SMS", 2000)
    if res["call"]:
        return {
            "message": "Hello world",
            "ttl": res["ttl"]
        }
    else:
        return {
            "message": "Too many request",
            "ttl": res["ttl"]
        }

class Th (Thread):
    def __init__(self, num):
        Thread.__init__(self)
        self.num = num
    def run(self):
        print(str(self.num) + " " + str(test()))

if __name__ == '__main__':
    # thread usando Redis para rate limit
   #for i in range(500):
   # a = Th(i)
   # a.start()

    # rate limiter interno
   rate_limiter = RateLimiter (max_calls = 2, period = 3, callback = limited)
   for i in range(5):
    with rate_limiter:
        print('Iteration ',i)