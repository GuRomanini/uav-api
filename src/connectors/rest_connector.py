from datetime import datetime, timezone
from abc import ABCMeta
import json
from requests import Response, request

from utils.logger import Logger
from utils.context import Context


class RestConnector(metaclass=ABCMeta):
    def __init__(self, context: Context, class_name, base_url, timeout) -> None:
        self.logger = Logger(context, class_name)
        self.base_url = base_url
        self.context = context
        self.timeout = timeout

    def send(
        self,
        endpoint,
        method,
        payload=None,
        headers={},
        data=None,
        cert=None,
        verify=True,
    ):

        headers["GlobalTraceId"] = self.context.global_trace_id
        url = f"{self.base_url}{endpoint}"

        if data:
            to_log_json = {"data": data}
        elif payload:
            to_log_json = {"payload": payload}
        else:
            to_log_json = {"payload": ""}

        self.logger.info(f"OUTGOING REQUEST {method} {url}", to_log_json)
        start = datetime.now(tz=timezone.UTC)

        if data:
            response = request(
                method.upper(),
                url,
                headers=headers,
                data=data,
                cert=cert,
                verify=verify,
            )
        else:
            response = request(
                method.upper(),
                url,
                headers=headers,
                json=payload,
                cert=cert,
                verify=verify,
            )

        end = datetime.now(tz=timezone.UTC)

        base_response = BaseConnectorResponse(
            endpoint=endpoint,
            method=method,
            payload=payload,
            headers=headers,
            start=start,
            end=end,
            response=response,
        )

        took = (end - start).total_seconds() * 1000

        to_log_json = {"payload": base_response.response_json or base_response.response.text}

        self.logger.info(
            f"INCOMING RESPONSE {response.status_code} {method} {url} {took} ms",
            to_log_json,
        )

        return base_response


class BaseConnectorResponse:
    def __init__(
        self,
        response: Response,
        endpoint: str,
        method: str,
        headers: dict,
        payload: dict,
        start: datetime,
        end: datetime,
    ) -> None:
        self.endpoint = endpoint
        self.method = method
        self.payload = payload
        self.headers = headers
        self.start = start
        self.end = end
        self.response = response
        self.response_content = response.content
        self.response_status = response.status_code

        self.response_json = None
        try:
            self.response_json = json.loads(self.response_content)
        except Exception:
            ...
            # logger warning


class BaseConnectorException(Exception):
    def __init__(self, base_response: BaseConnectorResponse) -> None:
        self.base_response = base_response
