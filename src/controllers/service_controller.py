from connectors import ServiceHandlerConnector
from utils.context import Context
from utils.logger import Logger


class ServiceController:
    def __init__(self, context: Context) -> None:
        self.context: Context = context
        self.logger = Logger(context, __class__)

    def register_service(self, service_data: dict) -> dict:
        self.logger.debug(f"Registering Service: {service_data['service_name']}")

        service_handler_connector = ServiceHandlerConnector(context=self.context)
        return service_handler_connector.register_service(
            service_name=service_data["service_name"], service_type=service_data["service_type"]
        )
