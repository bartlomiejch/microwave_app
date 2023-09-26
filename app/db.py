import sys

import redis


def create_redis():
    try:
        client = redis.ConnectionPool(
            host="redis", port=6379, db=0, decode_responses=True,
            password="password"
        )
        return client
    except redis.ConnectionError:
        print("Connection Error!")
        sys.exit(1)


pool = create_redis()
