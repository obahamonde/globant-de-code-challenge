from fastapi import FastAPI

from api.handlers import app as api_router
from prisma import Prisma


class PrismaApp(FastAPI):
    """Prisma + FastAPI + Pydantic + PostgreSQL Stack"""

    prisma: Prisma

    def __init__(self, *args, **kwargs):
        super().__init__(
            title="CSV API",
            description="CSV SQL API for globant coding challenge",
            *args,
            **kwargs
        )
        self.prisma = Prisma(auto_register=True, log_queries=True)
        self.add_event_handler("startup", self.on_startup)
        self.add_event_handler("shutdown", self.on_shutdown)

    async def on_startup(self):
        """Upon app startup, creates a persistent connection to the database
        through Prisma RPC client"""
        await self.prisma.connect()

    async def on_shutdown(self):
        """Upon app shutdown, closes the persistent connection to the database"""
        await self.prisma.disconnect()


def bootstrap() -> PrismaApp:
    """Application Instantiation and routes registration"""
    app = PrismaApp()
    app.include_router(api_router)
    return app
