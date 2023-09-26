import json


class JsonCacheManager:

    @staticmethod
    def set(cache, key, data):
        return cache.set(key, json.dumps(data))

    @staticmethod
    def get(cache, key):
        data = cache.get(key)
        if data:
            return json.loads(data)
        return