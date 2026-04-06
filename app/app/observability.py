import json
import logging
import sys
import time
import uuid


REQUEST_ID_HEADER = "X-Request-ID"
LOGGER_NAME = "app.request"


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)


def get_request_id(header_value: str | None) -> str:
    if header_value:
        return header_value.strip()
    return str(uuid.uuid4())


def log_request(*, request_id: str, method: str, path: str, status_code: int, duration_ms: float) -> None:
    logging.getLogger(LOGGER_NAME).info(
        json.dumps(
            {
                "event": "http_request",
                "request_id": request_id,
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": round(duration_ms, 2),
            }
        )
    )


def now() -> float:
    return time.perf_counter()
