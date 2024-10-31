from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

from fast_zero.middlewares.exception_middleware import http_exception_handler
from fast_zero.routers import auth, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)

app.exception_handler(StarletteHTTPException)(http_exception_handler)
