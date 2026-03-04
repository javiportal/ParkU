import json
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("parku")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration_ms = round((time.time() - start_time) * 1000, 2)
        request_id = getattr(request.state, "request_id", "N/A")

        log_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "level": "INFO",
            "request_id": request_id,
            "method": request.method,
            "endpoint": str(request.url.path),
            "duration_ms": duration_ms,
            "status_code": response.status_code,
        }

        logger.info(json.dumps(log_data))
        return response
