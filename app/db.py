import json
import sys

import redis


def create_redis():
    try:
        client = redis.ConnectionPool(
            host="redis", port=6379, db=0, decode_responses=True, password="password"
        )
        return client
    except redis.ConnectionError:
        print("Connection Error!")
        sys.exit(1)


pool = create_redis()


class RedisManager:
    def __init__(self, redis):
        self.redis = redis

    def set(self, key, data):
        self.redis.set(key, json.dumps(data))

    def get(self, key):
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return
