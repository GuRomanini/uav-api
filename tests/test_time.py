from qilocal.utils import Time
from os import environ
import requests
from random import randint


class TestTime:
    time = Time()
    endpoint = f'http://{environ["SERVER_LOCALHOST"]}:3000/time'

    def test_change_random_date_0(self):
        day = "%02d" % randint(1, 28)
        mon = "%02d" % randint(1, 12)
        year = randint(2000, 2050)
        hour = "%02d" % randint(0, 23)
        min = "%02d" % randint(0, 59)
        self.time.change(f"{year}-{mon}-{day}T{hour}:{min}Z")
        req = requests.get(self.endpoint)
        expected = {
            "day": int(day),
            "month": int(mon),
            "year": year,
            "hour": int(hour),
            "min": int(min),
        }
        assert req.json() == expected

    def test_change_random_date_1(self):
        day = "%02d" % randint(1, 28)
        mon = "%02d" % randint(1, 12)
        year = randint(2000, 2050)
        hour = "%02d" % randint(0, 23)
        min = "%02d" % randint(0, 59)
        self.time.change(f"{year}-{mon}-{day}T{hour}:{min}Z")
        req = requests.get(self.endpoint)
        expected = {
            "day": int(day),
            "month": int(mon),
            "year": year,
            "hour": int(hour),
            "min": int(min),
        }
        assert req.json() == expected

    def test_change_random_date_2(self):
        day = "%02d" % randint(1, 28)
        mon = "%02d" % randint(1, 12)
        year = randint(2000, 2050)
        hour = "%02d" % randint(0, 23)
        min = "%02d" % randint(0, 59)
        self.time.change(f"{year}-{mon}-{day}T{hour}:{min}Z")
        req = requests.get(self.endpoint)
        expected = {
            "day": int(day),
            "month": int(mon),
            "year": year,
            "hour": int(hour),
            "min": int(min),
        }
        assert req.json() == expected

    def test_change_random_date_3(self):
        day = "%02d" % randint(1, 28)
        mon = "%02d" % randint(1, 12)
        year = randint(2000, 2050)
        hour = "%02d" % randint(0, 23)
        min = "%02d" % randint(0, 59)
        self.time.change(f"{year}-{mon}-{day}T{hour}:{min}Z")
        req = requests.get(self.endpoint)
        expected = {
            "day": int(day),
            "month": int(mon),
            "year": year,
            "hour": int(hour),
            "min": int(min),
        }
        assert req.json() == expected

    def test_change_random_date_4(self):
        day = "%02d" % randint(1, 28)
        mon = "%02d" % randint(1, 12)
        year = randint(2000, 2050)
        hour = "%02d" % randint(0, 23)
        min = "%02d" % randint(0, 59)
        self.time.change(f"{year}-{mon}-{day}T{hour}:{min}Z")
        req = requests.get(self.endpoint)
        expected = {
            "day": int(day),
            "month": int(mon),
            "year": year,
            "hour": int(hour),
            "min": int(min),
        }
        assert req.json() == expected
