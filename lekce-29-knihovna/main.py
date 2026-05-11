from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from models import HealthResponse

# Aplikace + jediny stav serveru: jedna instance pizzerie.

app = FastAPI(title="Knihovna API", version="1.0.0")
#knihovna = Knihovna()


# ============================================================
# ENDPOINTY
# ============================================================

@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
