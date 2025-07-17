import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import static, tacticians, matches

app = FastAPI(title="TFT Tools API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev server
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(static.router)
# app.include_router(tacticians.router)
# app.include_router(matches.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
