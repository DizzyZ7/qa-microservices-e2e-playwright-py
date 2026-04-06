from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .errors import AppError
from .observability import REQUEST_ID_HEADER


def error_response(code: str, message: str, *, details=None, status_code: int, request_id: str | None = None):
    payload = {"error": {"code": code, "message": message}}
    if details is not None:
        payload["error"]["details"] = details
    if request_id is not None:
        payload["error"]["request_id"] = request_id
    response = JSONResponse(status_code=status_code, content=payload)
    if request_id is not None:
        response.headers[REQUEST_ID_HEADER] = request_id
    return response


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return error_response(
            exc.code,
            exc.message,
            status_code=exc.status_code,
            request_id=getattr(request.state, "request_id", None),
        )

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        if request.url.path.startswith("/api/") or request.url.path.startswith("/health"):
            if isinstance(exc.detail, dict):
                return error_response(
                    "service_unavailable",
                    "Service is not ready",
                    details=exc.detail,
                    status_code=exc.status_code,
                    request_id=getattr(request.state, "request_id", None),
                )
            return error_response(
                str(exc.detail).lower().replace(" ", "_"),
                str(exc.detail),
                status_code=exc.status_code,
                request_id=getattr(request.state, "request_id", None),
            )
        return await http_exception_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        if request.url.path.startswith("/api/"):
            details = [
                {
                    "field": ".".join(str(part) for part in error["loc"] if part != "body"),
                    "message": error["msg"],
                }
                for error in exc.errors()
            ]
            return error_response(
                "validation_error",
                "Request validation failed",
                details=details,
                status_code=422,
                request_id=getattr(request.state, "request_id", None),
            )
        return await http_exception_handler(request, HTTPException(status_code=422, detail=exc.errors()))
