import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SapPoEnvironmentConfig:
    name: str
    username: str
    password: str
    host: str


DEFAULT_ENVIRONMENT = os.environ.get("SAP_PO_ENV", "pod").lower()

_ENV_DEFAULTS = {
    "pod": {
        "username": "SUP.FRACASSG",
        "password": "vQH5c4y8bbg",
        "host": "http://sappod.menarini.net:54000",
    },
    "pid": {
        "username": "SUP.FRACASSG",
        "password": "Init123!",
        "host": "http://sappid.menarini.net:53100",
    },
    "pop": {
        "username": "SUP.FRACASSG",
        "password": "Init123!",
        "host": "http://sappopcs.menarini.net:50000",
    },
    "pip": {
        "username": "SUP.FRACASSG",
        "password": "Init123!",
        "host": "http://sappipcs.menarini.net:54100",
    },
}


def _env_var(environment: str, key: str) -> str:
    return f"SAP_PO_{environment.upper()}_{key}"


def get_environment_config(environment: str | None = None) -> SapPoEnvironmentConfig:
    environment_name = (environment or DEFAULT_ENVIRONMENT).lower()
    defaults = _ENV_DEFAULTS.get(environment_name)
    if defaults is None:
        valid_values = ", ".join(sorted(_ENV_DEFAULTS))
        raise ValueError(f"Ambiente SAP PO non valido '{environment_name}'. Valori ammessi: {valid_values}")

    return SapPoEnvironmentConfig(
        name=environment_name,
        username=os.environ.get(_env_var(environment_name, "USER"), os.environ.get("SAP_PO_USER", defaults["username"])),
        password=os.environ.get(_env_var(environment_name, "PASSWORD"), os.environ.get("SAP_PO_PASSWORD", defaults["password"])),
        host=os.environ.get(_env_var(environment_name, "HOST"), os.environ.get("SAP_PO_HOST", defaults["host"])),
    )


_DEFAULT_CONFIG = get_environment_config()
USERNAME = _DEFAULT_CONFIG.username
PASSWORD = _DEFAULT_CONFIG.password
HOST = _DEFAULT_CONFIG.host
DB_FILE = "sap_po_data.db"
