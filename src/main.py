from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Orbital Copilot Usage API")
app.include_router(router)
