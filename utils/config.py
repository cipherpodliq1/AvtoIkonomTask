import os
from dotenv import load_dotenv

load_dotenv()

_REQUIRED_ENV_VARS = ("BASE_URL", "QA_EMAIL", "QA_PASSWORD")


def _load_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        return ""
    return value


def _resolve_required_credentials() -> dict[str, str]:
    resolved = {name: _load_required_env(name) for name in _REQUIRED_ENV_VARS}
    missing = [name for name, value in resolved.items() if not value]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in the values, "
            + "or export them in your shell. CI injects them via GitHub Secrets."
        )
    return resolved


_credentials = _resolve_required_credentials()

BASE_URL = _credentials["BASE_URL"]
QA_EMAIL = _credentials["QA_EMAIL"]
QA_PASSWORD = _credentials["QA_PASSWORD"]
