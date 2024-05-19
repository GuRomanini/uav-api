import os
import falcon
from datetime import datetime

from constants import SERVICE_NAME


class Home:
    def on_get(self, req, resp):
        resp.status = falcon.code_to_http_status(200)
        resp.media = {SERVICE_NAME: SERVICE_NAME, f"{datetime.now()}": str(os.getpid())}
