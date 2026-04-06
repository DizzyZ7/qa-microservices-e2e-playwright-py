from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .db import dispose_engine, init_db
from .handlers import register_exception_handlers
from .observability import REQUEST_ID_HEADER, configure_logging, get_request_id, log_request, now
from .routers_api import router as api_router
from .routers_health import router as health_router
from .routers_ui import router as ui_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    init_db()
    app.state.is_ready = True
    try:
        yield
    finally:
        app.state.is_ready = False
        dispose_engine()


app = FastAPI(title="Demo Orders Service", lifespan=lifespan)
register_exception_handlers(app)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "testserver"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = get_request_id(request.headers.get(REQUEST_ID_HEADER))
    request.state.request_id = request_id
    started_at = now()
    response = await call_next(request)
    response.headers[REQUEST_ID_HEADER] = request_id
    log_request(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=(now() - started_at) * 1000,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


app.include_router(health_router)
app.include_router(api_router)
app.include_router(ui_router)
