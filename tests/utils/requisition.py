import json
from requests import request, Response
from os import environ


class ClientRequisition:
    @staticmethod
    def send(
        method,
        endpoint,
        payload=None,
        headers=None,
        data=None,
        cert=None,
        verify=True,
    ):

        if headers is None:
            headers = dict()

        base_url = f'http://{environ["SERVER_LOCALHOST"]}:{environ["API_PORT"]}/'

        url = f"{base_url}{endpoint}"

        response = request(
            method.upper(),
            url,
            headers=headers,
            json=payload,
            data=data,
            cert=cert,
            verify=verify,
        )

        base_response = BaseConnectorResponse(
            endpoint=endpoint,
            method=method,
            payload=payload,
            headers=headers,
            response=response,
        )

        return base_response

    def async_send(
        method,
        endpoint,
        payload=None,
        headers=None,
        data=None,
        cert=None,
        verify=True,
    ):

        if headers is None:
            headers = dict()

        base_url = f'http://{environ["SERVER_LOCALHOST"]}:{environ["API_PORT"]}/'

        url = f"{base_url}{endpoint}"

        response = request(
            method.upper(),
            url,
            headers=headers,
            json=payload,
            data=data,
            cert=cert,
            verify=verify,
        )

        base_response = BaseConnectorResponse(
            endpoint=endpoint,
            method=method,
            payload=payload,
            headers=headers,
            response=response,
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
    ) -> None:
        self.endpoint = endpoint
        self.method = method
        self.payload = payload
        self.headers = headers
        self.response = response
        self.response_content = response.content
        self.response_status = response.status_code

        self.response_json = None
        try:
            self.response_json = json.loads(self.response_content)
        except Exception as ex:
            print(ex)
            ...
            # logger warning
