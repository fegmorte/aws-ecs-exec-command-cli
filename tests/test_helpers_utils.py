from ecs_connect_cli.helpers import is_json


def test_is_json_with_object():
    assert is_json('{"name":"value"}') is True


def test_is_json_with_string():
    assert is_json("not-json") is False
