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
    def validate_existent_user_agent(req: Request) -> str:
        user_agent = req.headers.get("USER-AGENT")
        if user_agent is None:
            raise ForbiddenInexistentRequester()
        return user_agent
