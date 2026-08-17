import logging
import time

from fastapi import Request


logger = logging.getLogger("feedback_api")


async def log_request(
    request: Request,
    call_next,
):
    """
    Log incoming requests and their response time.
    """

    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed_time = (
        time.perf_counter() - start_time
    )

    logger.info(
        "%s %s -> %s (%.4f seconds)",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_time,
    )

    response.headers["X-Process-Time"] = (
        f"{elapsed_time:.4f}"
    )

    return response