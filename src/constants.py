from os import environ, path

SERVICE_ROOT = path.abspath(path.dirname(__file__))
SCHEMA_PATH = SERVICE_ROOT + "/schemas/"
BYPASS_ENDPOINTS = ["/", "/health_check"]

SERVICE_NAME = environ.get("SERVICE_NAME")
APP_ENV = environ.get("APP_ENV")

GCS_PROXY_ADDRESS = environ.get("GCS_PROXY_ADDRESS")

INTERNAL_TOKEN = environ.get("INTERNAL_TOKEN")


def check_variables():
    variable_names = [k for k in dir() if (k[:2] != "__" and not callable(globals()[k]))]
    variables_without_value = []
    for variable in variable_names:
        variable_value = globals()[variable]
        if isinstance(variable_value, int) and variable_value == -1:
            variables_without_value.append(variable)
        elif isinstance(variable_value, float) and variable_value == -1:
            variables_without_value.append(variable)
        elif isinstance(variable_value, str) and not variable_value:
            variables_without_value.append(variable)
    if variables_without_value:
        raise EnvironmentError(
            "A Error occurred while checking variables, please verify these variables without values {}".format(
                variables_without_value
            )
        )
