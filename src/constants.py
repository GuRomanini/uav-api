import os

ENV_ID = os.environ.get("ENV_ID")
SERVICE_ROOT = os.path.abspath(os.path.dirname(__file__))
SCHEMA_PATH = SERVICE_ROOT + "/schemas/"
BYPASS_ENDPOINTS = ["/", "/health_check"]

SERVICE_NAME = os.environ.get("SERVICE_NAME")
COMMIT = os.environ.get("COMMIT")
APP_ENV = os.environ.get("APP_ENV")
PROJECT_ENV = os.environ.get("PROJECT_ENV")


DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")

DB_HOST = load_vars("DB_HOST")
DB_PASSWORD = load_vars("DB_PASSWORD")
WEBHOOK_AUTH_TOKEN = load_vars("WEBHOOK_AUTH_TOKEN")
INTERNAL_TOKEN = load_vars("INTERNAL_TOKEN")
GENIEKEY = load_vars("GENIEKEY")
PRIVATE_KEY = load_vars("PRIVATE_KEY_TEST")
PUBLIC_KEY = load_vars("PUBLIC_KEY_TEST")

os.makedirs("/certs", exist_ok=True)
with open("/certs/private.crt", "w") as file:
    file.write(PRIVATE_KEY)
with open("/certs/public.crt", "w") as file:
    file.write(PUBLIC_KEY)
    
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
