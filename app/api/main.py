from fastapi import FastAPI
from datetime import datetime
from app.api.routers import query

app = FastAPI(title="RTIDSA API", version="0.1.0")
app.include_router(query.router, prefix="")


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/")
async def root() -> dict:
    return {"service": "Real-Time Intelligent Data Stream Query Assistant", "version": "0.1.0"}

