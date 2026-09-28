from fastapi import FastAPI

from app.routes.ask import router


app = FastAPI(
    title="Repository Research Agent",
    description="LangChain agent for researching GitHub repositories.",
    version="1.0.0",
)


app.include_router(router)