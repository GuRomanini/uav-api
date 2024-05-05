import uuid
from constants import GENIEKEY, APP_ENV, SERVICE_NAME

from utils.context import Context
from typing import Optional
from connectors.rest_connector import RestConnector


class OpsGenieConnector(RestConnector):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__, base_url="https://api.opsgenie.com", timeout=60)

    def send_alert(
        self,
        message: str,
        priority: str = None,
        description: Optional[str] = None,
        extra_properties: Optional[dict] = None,
        ignore_environment: bool = False,
        alias: str = str(uuid.uuid4()),
    ):
        """
        Alert Priority
        P1 - Critical - Will call QI Team and will be checked immediately
        P2 - High - Used as Team emergency, so will be checked as fast as possible by the correspondent team
        P3 - Moderate - Must be checked soon but can wait some minutes
        P4 - Low - Can be used as an TO DO alert to alert some task to be done for example
        P5 - Informational - Probably will not be used, since we do not use alerts to raise information

        Message is the synthetic information about the alerta, will be in the push notification
        Description is an OPTIONAL more detailed description about the alert
        Details is an OPTIONAL JSON to be shown in the OpsGenie Alert detailed view
        """

        details = {"global_trace_id": self.context.global_trace_id}
        if extra_properties is not None:
            details.update(extra_properties)

        alert_payload = {
            "message": f"[{APP_ENV.upper()}][{SERVICE_NAME.upper()}] {message}",
            "alias": alias,
            "priority": priority if priority in ["P1", "P2", "P3", "P4", "P5"] else "P3",
            "details": details,
        }
        if description is not None:
            alert_payload["description"] = description

        if APP_ENV.upper() != "LIVE" and ignore_environment is False:
            return
        try:
            alert_result = self.send(
                endpoint="/v2/alerts",
                method="POST",
                headers={"Authorization": "GenieKey " + GENIEKEY},
                payload=alert_payload,
            )
            return alert_result
        except Exception as e:
            self.logger.warning(msg=f"OpsGenie unavailable: {str(e)}")
            return None
