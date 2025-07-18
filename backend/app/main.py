# Load dotenv before everything
from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import accounts, static, summoners, matches

app = FastAPI(title="TFT Tools API")

# app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev server
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(static.router)
app.include_router(summoners.router)
app.include_router(matches.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
