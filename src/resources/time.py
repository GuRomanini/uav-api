import falcon
from datetime import datetime


class TimeResource:
    def on_get(self, req, resp):
        time_now = datetime.now()
        resp.status = falcon.code_to_http_status(200)
        resp.media = {
            "day": int("%02d" % time_now.day),
            "month": int("%02d" % time_now.month),
            "year": time_now.year,
            "hour": int("%02d" % time_now.hour),
            "min": int("%02d" % time_now.minute),
        }
