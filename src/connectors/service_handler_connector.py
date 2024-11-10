from utils.context import Context
from connectors.rest_connector import BaseConnectorException, BaseConnectorResponse, RestConnector

from constants import GCS_PROXY_ADDRESS, UAV_KEY


class ServiceHandlerConnector(RestConnector):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__, base_url=GCS_PROXY_ADDRESS, timeout=60)

    def register_uav(self, uav_name: str) -> dict:
        payload = {
            "uav_name": uav_name,
        }
        response: BaseConnectorResponse = self.send(
            endpoint="/uav", method="POST", payload=payload, headers={"roles": "master"}
        )

        if response.response_status != 201:
            raise BaseConnectorException(response)

        return response.response_json

    def register_service(self, service_name: str, service_endpoint: str) -> dict:
        payload = {
            "service_name": service_name,
            "uav_key": UAV_KEY,
            "base_url": service_endpoint,
        }
        response: BaseConnectorResponse = self.send(
            endpoint="/uav/service", method="POST", payload=payload, headers={"roles": "master"}
        )

        if response.response_status != 201:
            raise BaseConnectorException(response)

        return response.response_json
