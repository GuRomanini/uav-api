from errors import BaseException


class ForbiddenNotMaster(BaseException):
    code = "UCS000002"

    def __init__(self) -> None:
        title = "Forbidden"
        http_status = 403
        description = "You are not allowed to perform this action at this endpoint."
        translation = "Você não está autorizado a performar esta ação neste endpoint."
        super().__init__(title, self.code, http_status, description, translation)


class ForbiddenInexistentRequester(BaseException):
    code = "UCS000003"

    def __init__(self) -> None:
        title = "Forbidden"
        http_status = 403
        description = "This service cannot process requests without a 'SELECTED-AGENT'"
        translation = "Esse serviço não pode processar requisições sem o Header 'SELECTED-AGENT'"
        super().__init__(title, self.code, http_status, description, translation)


class ForbiddenNotInternal(BaseException):
    code = "UCS000004"

    def __init__(self) -> None:
        title = "Forbidden"
        http_status = 403
        description = "Request must be internal"
        translation = "Requisição precisa ser interna"
        super().__init__(title, self.code, http_status, description, translation)
