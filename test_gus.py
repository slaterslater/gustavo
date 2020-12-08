import gus
from src import args, out, urls


def test_get_status_good():
    status = urls.get_status("https://realpython.com/python-testing/")
    assert status["desc"] == "GOOD"


def test_get_status_fail():
    status = urls.get_status("http://badbad.bad")
    assert status["desc"] == "FAIL"


class TestCheckNested:
    def test_one(self):
        assert urls.check_nested("[http://test.com]") == "http://test.com"

    def test_two(self):
        assert urls.check_nested("http://test.com]") == "http://test.com]"

    def test_three(self):
        assert urls.check_nested("[http://test.com]]") == "http://test.com]"
