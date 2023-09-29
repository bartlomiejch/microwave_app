import json
from unittest.mock import Mock

import pytest

from app.db import RedisManager


@pytest.fixture
def mock_redis():
    return Mock()


@pytest.fixture
def redis_manager(mock_redis):
    return RedisManager(mock_redis)


def test_set_method(redis_manager, mock_redis):
    key = "test_key"
    data = {"foo": "bar"}

    result = redis_manager.set(key, data)

    mock_redis.set.assert_called_once_with(key, json.dumps(data))
    assert result is None


def test_get_method(redis_manager, mock_redis):
    key = "test_key"
    mock_redis.get.return_value = json.dumps({"foo": "bar"})

    result = redis_manager.get(key)

    mock_redis.get.assert_called_once_with(key)
    assert result == {"foo": "bar"}


def test_get_method_with_missing_key(redis_manager, mock_redis):
    key = "non_existent_key"
    mock_redis.get.return_value = None

    result = redis_manager.get(key)

    mock_redis.get.assert_called_once_with(key)
    assert result is None


def test_get_method_with_invalid_json(redis_manager, mock_redis):
    key = "test_key"
    mock_redis.get.return_value = "invalid_json"

    with pytest.raises(ValueError):
        redis_manager.get(key)
