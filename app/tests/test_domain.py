import json
from unittest.mock import Mock

import pytest

from app.domain import Equipment, Microwave


def test_equipment_initial_state():
    equipment = Equipment()
    assert equipment.power == 0
    assert not equipment.is_on


def test_equipment_power_up():
    equipment = Equipment()
    equipment.power_up()
    assert equipment.power == 0
    assert not equipment.is_on


def test_equipment_power_down():
    equipment = Equipment()
    equipment.power_up()
    equipment.power_down()
    assert equipment.power == 0
    assert not equipment.is_on


def test_equipment_cancel():
    equipment = Equipment()
    equipment.power_up()
    equipment.cancel()
    assert equipment.power == 0
    assert not equipment.is_on


def test_microwave_initial_state():
    microwave = Microwave()
    assert microwave.power == 0
    assert not microwave.is_on
    assert microwave.counter == 0


def test_microwave_power_up():
    microwave = Microwave()
    microwave.power_up()
    assert microwave.power == 10
    assert microwave.is_on


def test_microwave_power_down():
    microwave = Microwave()
    microwave.power_up()
    microwave.power_down()
    assert microwave.power == 0
    assert not microwave.is_on


def test_microwave_counter_up():
    microwave = Microwave()
    microwave.counter_up()
    assert microwave.counter == 10


def test_microwave_counter_down():
    microwave = Microwave()
    microwave.counter_up()
    microwave.counter_down()
    assert microwave.counter == 0


def test_microwave_load():
    microwave = Microwave()
    data = {"power": 50, "counter": 1800, "is_on": True}
    microwave.load(data)
    assert microwave.power == 50
    assert microwave.counter == 1800
    assert microwave.is_on


def test_microwave_cancel():
    microwave = Microwave()
    microwave.counter_up()
    microwave.cancel()
    assert microwave.counter == 0
    assert microwave.power == 0
    assert not microwave.is_on


def test_microwave_get_message():
    microwave = Microwave()
    microwave.power_up()
    message = microwave.get_message()
    assert message == "Power increased to 10%"


def test_microwave_get_state():
    microwave = Microwave()
    microwave.power_up()
    state = microwave.get_state()
    expected_state = {"counter": 0, "is_on": True, "power": 10}
    assert state == expected_state
