from errors import BaseException


class InvalidSchema(BaseException):
    code = "UCS000001"

    def __init__(self, __description) -> None:
        title = "Bad Request"
        http_status = 400
        description = __description
        translation = "Schema Inválido"
        super().__init__(title, self.code, http_status, description, translation)
