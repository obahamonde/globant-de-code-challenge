from functools import *
from typing import *

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from prisma import Prisma

Handler = Callable[[Request], Awaitable[Response]]

H = TypeVar("H", bound=Handler)

class Decorator(Generic[H]):
    def __call__(self, handler: H) -> H:
        @wraps(handler)
        async def wrapper(request: Request) -> Response:
            print(request)
            return await handler(request)
        return cast(H, wrapper)
    
@Decorator()
async def handler(request: Request) -> Response:
    return Response("Hello World")

