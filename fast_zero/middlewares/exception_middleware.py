from fastapi import HTTPException, Request
from starlette.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={'message': exc.detail}
    )
