from falcon import Response

from utils.context import Context
from connectors.rest_connector import BaseConnectorException, BaseConnectorResponse, RestConnector

from constants import SERVICE_HANDLER_API_ADDRESS

class ServiceHandlerConnector(RestConnector):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__, base_url=SERVICE_HANDLER_API_ADDRESS, timeout=60)

    def register_service(self, service_name: str, service_type: str) -> dict:
        payload = {
            "service_name": service_name,
            "service_type": service_type
        }
        response: BaseConnectorResponse = self.send(endpoint="/service", method="POST", payload=payload, headers={"roles": "master"})

        if response.response_status != 201:
            raise BaseConnectorException(response)
        
        return response.response_json
