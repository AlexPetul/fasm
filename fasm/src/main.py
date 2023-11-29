from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.sections.router import router as sections_router


def get_application() -> FastAPI:
    application = FastAPI()

    # Middleware settings
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    application.include_router(auth_router, prefix="/api")
    application.include_router(sections_router, prefix="/api")

    return application


app = get_application()
