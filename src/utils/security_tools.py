from errors import (
    ForbiddenNotMaster,
    ForbiddenInexistentRequester,
    ForbiddenNotInternal,
)

from constants import INTERNAL_TOKEN

from falcon import Request


class SecurityTools:
    @staticmethod
    def validate_master_request(req: Request) -> None:
        user_roles = req.headers.get("ROLES", "").split(",")
        is_master = "master" in user_roles
        if not is_master:
            raise ForbiddenNotMaster()

    @staticmethod
    def validate_internal_request(req: Request) -> None:
        internal_token = req.headers.get("INTERNAL-TOKEN")
        if internal_token != INTERNAL_TOKEN:
            raise ForbiddenNotInternal()

    @staticmethod
    def validate_existent_selected_agent(req: Request) -> str:
        selected_agent_key = req.headers.get("SELECTED-AGENT")
        if selected_agent_key is None:
            raise ForbiddenInexistentRequester()
        return selected_agent_key
